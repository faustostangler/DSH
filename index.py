import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
    
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Define a list of pages and their subpages using dash.page_registry.values()
pages = list(dash.page_registry.values())

# Define the App Names
title = "Análise Fundamentalista"
footer = 'Copyright © 2023 FSVGS'

# Define the main navigation sidebar
sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=False,
            pills=True,
            className="bg-dark",
)

# Define the secondary navigation sidebar that shows the sub-items based on the nav selection
subnav = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(subpage["name"], className="ms-4"),
            ],
            href=subpage["path"],
            active="exact",
        )
        for page in pages
        for subpage in page.get("subpages", [])
    ],
    vertical=True,
    pills=True,
    className="bg-light",
)


# Define the app layout
app.layout = dbc.Container([
    # Title
    dbc.Row([
        dbc.Col([
            html.H1(title),
        ]),
    ]),

    # Horizontal menu row
    dbc.Row([
        dbc.Col([
            sidebar,
        ]),
    ]),

    # Content
    dbc.Row([
        # Sub menu
        dbc.Col([
            'future submenu here',
            dbc.Col(subnav,),
            ], 
            xs=4, sm=4, md=2, lg=2, xl=2, xxl=2,
        ),
        # Content
        dbc.Col([
            dash.page_container
            ], 
            xs=8, sm=8, md=10, lg=10, xl=10, xxl=10,
        ),
]),

    # Footer
    dbc.Row([
        dbc.Col([
            footer,
        ], id='footer'),
    ]),

    ], fluid=True)





if __name__ == "__main__":
    app.run_server(debug=True)
