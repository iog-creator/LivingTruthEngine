import dash
from dash import dcc, html
import plotly.express as px
import os

app = dash.Dash(__name__)

# Example dashboard layout
app.layout = html.Div([
    html.H1('Living Truth Dashboard'),
    dcc.Graph(
        id='example-graph',
        figure=px.scatter_3d()
    )
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True) 