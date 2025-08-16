
import dash
import plotly.express as px
from dash import dcc, html

app = dash.Dash(__name__)

# Example dashboard layout
app.layout = html.Div(
    [
        html.H1("Living Truth Dashboard"),
        dcc.Graph(id="example-graph", figure=px.scatter_3d()),
    ]
)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
