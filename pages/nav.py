from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app

layout = html.Div([
    # Navigation links
    dbc.Nav([
        dbc.NavLink("Home", href="/home", id="home"),
        dbc.NavLink("Setor", href="/setor", id="setor"),
        dbc.NavLink("Subsetor", href="/subsetor", id="subsetor"),
        dbc.NavLink("Segmento", href="/segmento", id="segmento"),
        dbc.NavLink("Companhia", href="/companhia", id="companhia"),
    ], vertical=False, pills=False)
])

# Callbacks for this page...
