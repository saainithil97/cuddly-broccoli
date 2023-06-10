from grafanalib import core

dashboard = core.Dashboard(
    version=1,
    title="Sample dashboard",
    description="Sample dashboard from prometheues datasource",
    tags=[
        'sample',
    ],
    timezone="browser",
    editable=False,
    time= core.Time('now-30m', 'now'),
    panels=[],
).auto_panel_ids()