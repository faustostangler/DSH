from dash import html, dcc, exceptions
from dash.dependencies import Input, Output

from app import app
from assets.graphs import graphs_1, graphs_2

import assets.helper as b3
import assets.functions as run

import os
import pandas as pd
import numpy as np
import plotly.express as px
import gzip
import io
import base64

def decompress_data(compressed_data):
    """
    Decompress and decode the provided data.

    Parameters:
    - compressed_data (str): Compressed and encoded data.

    Returns:
    - pd.DataFrame: Decompressed and decoded data as a DataFrame.
    """
    buffer = io.BytesIO(base64.b64decode(compressed_data))
    with gzip.GzipFile(fileobj=buffer, mode='r') as f:
        df = pd.read_parquet(f)
    return df

def generate_callback(line_num, title, info):
    @app.callback(
        Output(f'graph-{line_num}', 'figure'),
        [Input('company-df', 'data')]
    )
    def update_graph(compressed_data):
        # Ensure compressed_data is string and not None or other type
        if not isinstance(compressed_data, str):
            print("PreventUpdate triggered: compressed_data is not a string.")
            raise exceptions.PreventUpdate("Data is not valid")

        df = decompress_data(compressed_data)
        tickers = np.sort(df['TICKER'].unique())
        df_ticker = []
        for ticker in tickers:
            df_ticker.append(df[df['TICKER'] == ticker])
        df = df_ticker[0]
        
        print(f'{ticker} df[0] attention please {tickers}')

        # Assuming plot_tweak function exists in your `run` module
        fig = run.plot_tweak(df, info['data'], info['options'])
        return fig

    return update_graph

# Generate callbacks using lines
for i, (title, info) in enumerate(graphs_1.items()):
    generate_callback(i, title, info)

# Preparing components before layout
additional_components = [(
    html.H2('secao graphs_1', id=f'graph-title-{i}'), 
)]
for i, (line, info) in enumerate(graphs_1.items()):
    additional_components.extend([
        html.H5(line, id=f'graph-title-{i}'), 
        html.P(info['description'], id=f'graph-line-{i}'), 
        dcc.Graph(id=f'graph-{i}')
    ])

# ----- LAYOUT -----
layout = html.Div([
    # Storing data to be passed between callbacks
    dcc.Store(id='company-df', storage_type='session'), 

    # Loading spinner that appears while callbacks are performed
    dcc.Loading(
        id="loading",
        type="circle",
        children=[
            # Main titles of the page
            html.H1("Análise Fundamentalista"),
            html.H2(id='company-segmento-title'), 
            html.H2(id='company-title'),
            
            # Additional components like graphs, tables, etc.
            *additional_components,
            # More contents here...
        ]
    )
])

# ----- CALLBACKS -----
@app.callback(
    [
        Output('company-segmento-title', 'children'),
        Output('company-title', 'children'),
        Output('company-df', 'data')
    ],  
    [
        Input('store-selected-company', 'data'),
        Input('store-selected-setor', 'data'),
        Input('store-selected-subsetor', 'data'),
        Input('store-selected-segmento', 'data')
    ]
)
def update_titles(stored_company, stored_setor, stored_subsetor, stored_segmento):
    """
    Update titles and load data based on selected company, setor, subsetor, and segmento.

    Parameters:
    - stored_company (dict): Stored selected company data.
    - stored_setor (dict): Stored selected setor data.
    - stored_subsetor (dict): Stored selected subsetor data.
    - stored_segmento (dict): Stored selected segmento data.

    Returns:
    - str: Updated segmento title.
    - str: Updated company title.
    - dict: Compressed and encoded company data.
    """
    # Check if the company data is available, if not, prevent the update
    if None in [stored_company]:
        raise exceptions.PreventUpdate
    
    # Extract the stored values
    companhia = stored_company.get('company', '')
    setor = stored_setor.get('setor', '')
    subsetor = stored_subsetor.get('subsetor', '')
    segmento = stored_segmento.get('segmento', '')
    
    # Initialize the titles and dataframe
    df = pd.DataFrame()
    segmento_title = ''
    company_title = ''
    
    # Load data and construct titles when a company is selected
    if companhia:
        # Construct the path to the file
        file = os.path.join(f'{b3.app_folder}company/{companhia}')
        
        # Check if the file exists and load the data
        if os.path.exists(file+'.pkl'):
            df = run.load_pkl(file)
        else:
            print(f"No data file found for company: {companhia}")

        # Construct the titles
        segmento_title = f"{setor} - {subsetor} - {segmento}"
        company_title = companhia

    # Compress and encode data for efficient storage
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode='w') as f:
        df.to_parquet(f)
    compressed_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return segmento_title, company_title, compressed_data
