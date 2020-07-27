import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot


def get_line_graph(x, y):

    x = np.array(x)
    y = np.array(y)
    data = go.Scatter(x=x, y=y)

    fig = go.Figure()
    fig.add_trace(data)

    layout = go.Layout(title="chart")
    pass
    layout.xaxis.title = "Seconds"
    layout.yaxis.title = "Volts"

    fig.layout = layout
    return plot(fig,
                output_type="div")
