from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app

layout = html.Div([
    # Navigation links
    dbc.Nav([
        dbc.NavLink("Dashboard", href="/dashboard", id="dashboard"),
        dbc.NavLink("Setor", href="/setor", id="setor"),
        dbc.NavLink("Subsetor", href="/subsetor", id="subsetor"),
        dbc.NavLink("Segmento", href="/segmento", id="segmento"),
    ], vertical=False, pills=False)
])

# Callbacks for this page...
