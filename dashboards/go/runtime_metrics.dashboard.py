import sys
import os.path
sys.path.insert(0, os.path.dirname(__file__))
from _grafanalib import (
    TimeSeries, DEFAULT_CALCS
)
from grafanalib import core
from grafanalib import formatunits as units

process_memory_targets=[
    core.Target(
        expr='process_resident_memory_bytes{job=~\"^($job)$\"}',
        legendFormat="resident",
        refId='A',
        metric="process_resident_memory_bytes"
    ),
    core.Target(
        expr='process_virtual_memory_bytes{job=~\"^($job)$\"}',
        legendFormat="virtual",
        refId='B',
        metric="process_virtual_memory_bytes"
    )
]

process_memory_deriv_targets=[
    core.Target(
        expr='rate(process_resident_memory_bytes{job=~\"^($job)$\"}[$interval])',
        legendFormat="resident",
        refId='A',
        metric="process_resident_memory_bytes"
    ),
    core.Target(
        expr='deriv(process_virtual_memory_bytes{job=~\"^($job)$\"}[$interval])',
        legendFormat="virtual",
        refId='B',
        metric="process_virtual_memory_bytes"
    )
]

go_goroutines=[
    core.Target(
        expr='go_goroutines{job=~\"^($job)\"}',
        legendFormat="{{job}} - goroutines",
        refId='A',
        metric="go_goroutines"
    ),
]

go_gc_duration_seconds=[
    core.Target(
        expr='go_gc_duration_seconds{job=~\"^($job)\"}',
        legendFormat="{{job}} - {{ quantile }}",
        refId='A',
        metric="go_gc_duration_seconds"
    ),
]

go_memstats_alloc_bytes=[
    core.Target(
        expr='go_memstats_alloc_bytes{job=~\"^($job)\"}',
        legendFormat="{{job}} - - bytes allocated",
        refId='A',
        metric="go_memstats_alloc_bytes"
    ),
    core.Target(
        expr='go_memstats_stack_inuse_bytes{job=~\"^($job)\"}',
        legendFormat="{{job}} - stack inuse",
        refId='B',
        metric="go_memstats_stack_inuse_bytes"
    ),
     core.Target(
        expr='go_memstats_heap_inuse_bytes{job=~\"^($job)\"}',
        legendFormat="{{job}} - heap inuse",
        refId='C',
        metric="go_memstats_heap_inuse_bytes"
    ),
    core.Target(
        expr='rate(go_memstats_alloc_bytes_total{job=~\"^($job)\"}[30s])',
        legendFormat="{{job}} - alloc rate",
        refId='D',
        metric="go_memstats_alloc_bytes_total"
    ),
]

process_open_fds = [
    core.Target(
        expr='process_open_fds{job=~\"^($job)\"}',
        legendFormat="{{job}} open fds",
        refId='A',
        metric="process_open_fds"
    ),
]

dashboard = core.Dashboard(
    version=1,
    title="Go runtime metrics",
    description="Go runtime metrics dashboard from prometheues datasource",
    tags=[
        'umap',
        'network layer',
        'go',
        'runtime'
    ],
    timezone="browser",
    editable=False,
    time= core.Time('now-30m', 'now'),
    templating=core.Templating(
        list= [
            core.Template(
                hide=0,
                default="5m",
                name="interval",
                type="interval",
                query="1m,5m,10m,30m,1h",
                refresh=2
            ),
            core.Template(
                dataSource="Prometheus",
                hide=0,
                name="job",
                type="query",
                query="label_values(go_goroutines, job)",
                refresh=2
            )
        ]
    ),
    panels=[        
        TimeSeries(
            title="process memory",
            gridpos=core.GridPos(h=8, w=12, x=0, y=0),
            targets= process_memory_targets,
            unit=units.BYTES_IEC,
            calcs=DEFAULT_CALCS
        ),
        TimeSeries(
            title="process memory deriv",
            gridpos=core.GridPos(h=8, w=12, x=12, y=0),
            targets= process_memory_deriv_targets,
            unit=units.BYTES_IEC,
            calcs=DEFAULT_CALCS
        ),
        TimeSeries(
            title="Goroutines",
            gridpos=core.GridPos(h=8, w=12, x=0, y=8),
            targets= go_goroutines,
            unit=units.SHORT,
            calcs=DEFAULT_CALCS
        ),
        TimeSeries(
            title="GC duration quantiles",
            gridpos=core.GridPos(h=8, w=12, x=12, y=8),
            targets= go_gc_duration_seconds,
            unit=units.SHORT,
            calcs=DEFAULT_CALCS
        ),
        TimeSeries(
            title="go memstats",
            gridpos=core.GridPos(h=8, w=12, x=0, y=16),
            targets= go_memstats_alloc_bytes,
            unit=units.BYTES_IEC,
            calcs=DEFAULT_CALCS
        ),        
        TimeSeries(
            title="process open fds",
            gridpos=core.GridPos(h=8, w=12, x=12, y=16),
            targets= process_open_fds,
            unit=units.SHORT,
            calcs=DEFAULT_CALCS
        ),        
    ],
).auto_panel_ids()