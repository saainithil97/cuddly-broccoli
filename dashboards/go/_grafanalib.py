from grafanalib import core

# Constants
DEFAULT_CALCS=["mean", "max", "min", "lastNotNull"]

# Helper function to create a TimeSeries panel
def TimeSeries(title, gridpos, targets,unit, calcs):
    return core.TimeSeries(
        colorMode="palette-classic",
        title=title,
        fillOpacity=10,    
        dataSource='Prometheus',
        showPoints="never",
        targets=targets,
        lineWidth=2,
        unit=unit,
        gridPos=gridpos,
        legendDisplayMode="table",
        legendCalcs=calcs
    )
