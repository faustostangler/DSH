import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app
from pages import sidebar, nav, home, setor, subsetor, segmento, companhia, setup

import assets.helper as b3
import assets.functions as run
 
import pandas as pd

# ----- LAYOUT -----
app.layout = html.Div([
    # Include navigation layout
    nav.layout, 
    # Horizontal line for separation
    html.Hr(),
    # URL component to track the current pathname
    dcc.Location(id='url', refresh=False),
    # Data stores to maintain selections across pages
    dcc.Store(id='store-selected-setor', storage_type='session'),
    dcc.Store(id='store-selected-subsetor', storage_type='session'),
    dcc.Store(id='store-selected-segmento', storage_type='session'),
    dcc.Store(id='store-selected-company', storage_type='session'),
    # Main layout divided into two columns: Sidebar and Content
    dbc.Row([
        dbc.Col([
            dbc.Row([
                sidebar.layout  # Include sidebar layout
            ], id='sidebar'), 
            dbc.Row([], id='nav')  # Placeholder for additional navigation (if needed)
        ], width=2),  # Sidebar takes up 2 out of 12 grid columns
        dbc.Col(id="content", width=10),  # Content takes up the remaining 10 columns
    ])
])

# ----- CALLBACKS -----
# Define callback to render page content based on URL
@app.callback(Output("content", "children"), 
              [Input("url", "pathname")])
def render_page_content(pathname):
    """
    Determine which layout to display based on the current URL/pathname.
    If the pathname matches a predefined route, return the corresponding page layout.
    If not, return a 404 "Not found" message.
    """
    # Define page routing
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
    # If pathname does not match any predefined route, display a 404 message
    else:
        return dbc.Card([
            dbc.CardBody([
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname '{pathname}' was not recognised..."),
            ])
        ], className='mt-5')

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_props_check=True)
    app.run_server(port=8051, debug=True)
