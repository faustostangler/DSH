from dash import html, dcc
from dash.dependencies import Input, Output
from app import app
import assets.helper as b3
import assets.functions as run
import pandas as pd

# ----- LAYOUT -----
# Define the layout for a specific page in the app
layout = html.Div([
    
    # Main title
    html.H1("Análise Fundamentalista"),

    # Space for visual separation
    html.H2(" "),

    # Loading component to provide a loading spinner for background data loading
    dcc.Loading(
        id="loading",
        type="circle",
        children=[
            # Interval component triggers the data loading function at specified intervals
            dcc.Interval(
                id='interval-load-data',
                interval=1*1000,  # 1 second interval
                n_intervals=0,
                max_intervals=1  # Stops after 1st interval to prevent continuous loading
            ),
            
            # Placeholder or component to display a data stat during loading
            html.H4(id='indicator-total-companies'),
        ]
    ),
])

# ----- CALLBACKS -----
