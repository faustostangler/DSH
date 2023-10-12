import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app
from pages import sidebar, nav, home, setor, subsetor, segmento, companhia, setup

import assets.helper as b3
import assets.functions as run

import pandas as pd

app.layout = html.Div([
    nav.layout, 
    html.Hr(),
    dcc.Location(id='url', refresh=False),  

    dcc.Store(id='store-selected-setor', storage_type='session'),
    dcc.Store(id='store-selected-subsetor', storage_type='session'),
    dcc.Store(id='store-selected-segmento', storage_type='session'),
    dcc.Store(id='store-selected-company', storage_type='session'),

    dbc.Row([
        dbc.Col([
            dbc.Row([
            sidebar.layout
            ], id='sidebar'), 
            dbc.Row([
            # nav.layout
            ], id='nav')
            
        ], width=2),
        dbc.Col(id="content", width=10),
    ])
])

@app.callback(Output("content", "children"), 
              [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ['/', "/home"]:
        return home.layout
    elif pathname == "/setor":
        return setor.layout
    elif pathname == "/subsetor":
        return subsetor.layout
    elif pathname == "/segmento":
        return segmento.layout
    elif pathname == "/companhia":
        return companhia.layout

    return dbc.Card([
        dbc.CardBody([
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname '{pathname}' was not recognised..."),
        ])
    ], className='mt-5')






















if __name__ == "__main__":
    app.run_server(port=8051, debug=True)
