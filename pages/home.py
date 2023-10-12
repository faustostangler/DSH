from dash import html, dcc
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    html.H2("Home Page"),
    dcc.Graph(id='graph-home'),
    # Your contents here...
])

# Callbacks for this page...
