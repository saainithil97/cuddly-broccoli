# Dashboard as code

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Problem statement](#problem-statement)
- [Solution](#solution)
- [Setup](#setup)
  - [Setting up grafana on local machine](#setting-up-grafana-on-local-machine)
  - [Install grafanalib](#install-grafanalib)
  - [Generate dashboards](#generate-dashboards)
  - [Vscode extensions](#vscode-extensions)
- [How to](#how-to)
  - [Writing dashboards](#writing-dashboards)
  - [Writing alerts](#writing-alerts)
- [Conclusion](#conclusion)
- [Future scope](#future-scope)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

(documents how grafana dashboards can be written as code)

## Problem statement
Application metrics are exposed on `/metrics` endpoint, which serves both as documentation and also a way for prometheus collector to scrape the metrics. While I'm writing this document, the only way for us to visualize these metrics is to use the prometheus UI or grafana, which is not ideal for the following reasons:
- The monitoring process is disconnected; we add metrics to the code-base as part of development, but we cannot visualize them until we create a dashboard for them
- Dashboards and alerts have to be created manually
- They are not version controlled
- They are not reproducible on local environment
- They are not reusable (the same dashboard cannot be used for multiple environments)

## Solution

Grafana lets you import dashboards as json files. These json files can be generated using different tools. The json files can be version controlled and can be used to generate json files for different environments. The json files can be imported into grafana using the grafana API.

The json files can be generated using
- jsonnet (with graffonet plugins maintained by grafana)
- grabana (go library)
- grafanalib (python library) -- preferred

## Setup

### Setting up grafana on local machine

In your local docker-compose.yaml file, add the following snippet
```yaml
version: "3.8"
services:
    # local setup for prometheus
    # you can reach prometheus on http://localhost:9090
    prometheus:
        image: prom/prometheus:v2.30.3
        ports:
        - 9090:9090
        volumes:
        # mount point for prometheus config file
        - ./assets/prometheus:/etc/prometheus
        # mount point for prometheus data where all the metrics will be stored
        - prometheus-data:/prometheus
        command: --web.enable-lifecycle  --config.file=/etc/prometheus/prometheus.yaml

    # local setup for grafana 
    # you can reach grafana on http://localhost:3000
    # includes
    # - prometheus datastore
    # - go runtime metrics dashboard
    # - http metrics dashboard
    grafana:
        image: grafana/grafana:9.1.7
        ports:
        - 3000:3000
        restart: unless-stopped
        volumes:
        # mount point for grafana data where all the dashboards and data will be stored
        - grafana-data:/var/lib/grafana        
volumes:
  prometheus-data:
  grafana-data:
```

This will setup prometheus and grafana on your local machine. You can reach prometheus on http://localhost:9090 and grafana on http://localhost:3000. You can login to grafana using the default credentials `admin:admin`. You can find the prometheus config file in `assets/prometheus/prometheus.yaml`. 

With the above setup you can manually create dashboards on grafana with prometheus as the datastore. But we are not going to stop here, lets see how we can generate dashboards as code.

### Compose up

To start the containers, run the following command
```bash
docker-compose up -d
```

### Install grafanalib

grafanalib is a python library that lets you generate grafana dashboards as json files. You can find more information about grafanalib [here](https://grafanalib.readthedocs.io/en/stable/) and the source code [here](https://github.com/weaveworks/grafanalib).

```bash
pip install grafanalib
```

### Generate dashboards
To generate the dashboards using grafanalib, you need to write a python script that uses the grafanalib library to generate the dashboards. You can find a sample dashboard in `assets/dashboards/sample.dashboard.py`. You can generate the json file using the following command

```bash
cd assets/dashboards
generate-dashboard -o sample.dashboard.json sample.dashboard.py
```

We can now generate the json file which can be imported to grafana. But we need to do this manually everytime we make a change to the dashboard. Lets see how we can automate this.

### Hot reloading dashboards

Grafana scans the folder `/etc/grafana/provisioning` every 10 seconds for changes and provisions the dashboards and datastores accordingly. You can find more information about provisioning in the [grafana docs](https://grafana.com/docs/grafana/latest/administration/provisioning/). You can mount the folder `assets/grafana` to `/etc/grafana/provisioning` in the docker-compose.yaml file as shown below.

Grafana will provision 
- all the datastores in the `assets/grafana/datastores` folder, you can find a sample prometheus datastore in the folder
- all the dashboards in the `assets/grafana/dashboards` folder, you can find sample go runtime metrics and http metrics dashboards in the folder

```yaml
grafana:
    image: grafana/grafana:9.1.7
    ports:
    - 3000:3000
    restart: unless-stopped
    volumes:
    # mount point for grafana data where all the dashboards and data will be stored
        - grafana-data:/var/lib/grafana        
    # grafana lets you provision dashboards and datasources from yaml files
    # Refer: https://grafana.com/docs/grafana/latest/administration/provisioning/#dashboards
        - ./assets/grafana:/etc/grafana/provisioning
    # mount point for dashboards, check assets/grafana/provisioning/dashboards for usage
        - ./assets/dashboards:/etc/dashboards
```

Now you can generate the json files and place them in the `assets/grafana/dashboards` folder. Grafana will automatically provision the dashboards. You can find the go runtime metrics and http metrics dashboards in the grafana UI.

### Vscode extensions

If you are using vscode, you can install the run on save extension to automatically generate the json files on save. You can find the extension [here](https://marketplace.visualstudio.com/items?itemName=emeraldwalk.RunOnSave).

Copy the following snippet to your vscode settings.json file to generate the json files on save
```json
"emeraldwalk.runonsave": {
        "commands": [
            {
                "match": "\\.dashboard.py$",
                "cmd": "/opt/homebrew/bin/generate-dashboard -o ${file}.json ${file}"
            },
        ]
    },
```

## How to

To add dashboards to grafana, you need to create a yaml file under assets/grafana/dashboards folder. The yaml file should have the following structure

```yaml
apiVersion: 1
providers:
# provider name
- name: 'default' 
# name of the folder in grafana, if empty, the dashboard will be added to the root folder
  folder: '' 
# type of the provider, file means the dashboards will be loaded from a file
  type: file 
# if true, the dashboards cannot be deleted from the UI
  disableDeletion: false 
# if true, the dashboards can be edited from the UI  
  editable: true 
# if true, the dashboards can be updated from the UI  
  allowUiUpdates: true 
# interval in seconds to scan for changes in the dashboards
updateIntervalSeconds: 10 
  options: 
  # path to the dashboards folder (this is the mounted path not the path on the local machine)
    path: /etc/dashboards 
  # if true, the folder structure will be created based on the folder structure in the false dashboards folder
    foldersFromFilesStructure: 
```

### Write dashboards

... 

### Write alerts

... 