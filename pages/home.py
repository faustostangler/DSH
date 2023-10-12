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
            dcc.Store(id='store-df-fund'),  # Store for the dataframe
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


# Callbacks for this page...
@app.callback(
    Output('store-df-fund', 'data'),
    Input('interval-load-data', 'n_intervals')
)
def load_and_store_data(_):
    # df = run.load_pkl('df_fund')
    df = pd.DataFrame()
    return df.to_dict('records')

# Callback to update the graph and the indicators using the stored dataframe
@app.callback(
     Output('indicator-total-companies', 'children'),
    Input('store-df-fund', 'data')
)
def update_content(data):
    df = pd.DataFrame(data)
    
    # Update the graph
    # ... graph update code here ...
    # graph_figure = ...

    # Update the indicator
    total_companies =len(df)
    indicator_text = f"Total Unique Companies: {total_companies}"

    return indicator_text
