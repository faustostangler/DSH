from dash import html, dcc
from dash.dependencies import Input, Output

from app import app

import assets.helper as b3
import assets.functions as run

import pandas as pd

layout = html.Div([
    html.H1("Análise Fundamentalista"),
    html.H2(" "),
    dcc.Loading(
        id="loading",
        type="circle",
        children=[
            dcc.Interval(
                id='interval-load-data',
                interval=1*1000,  # in milliseconds
                n_intervals=0,
                max_intervals=1  # stops the interval after 1 update
            ),
            html.H4(id='indicator-total-companies'),
            # ... other components to display other stats ...
        ]
    ),
])


