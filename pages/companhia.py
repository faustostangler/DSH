from dash import html, dcc, exceptions
from dash.dependencies import Input, Output

from app import app

import assets.helper as b3
import assets.functions as run

import pandas as pd
import os
import base64
import gzip
import io


layout = html.Div([
    dcc.Store(id='company-df', storage_type='session'), 

    dcc.Loading(
        id="loading",
        type="circle",  # "default", "cube", "circle", "cube", "dot", "cube", or "cube"
        children=[
            html.H1("Análise Fundamentalista"),
            html.H2(id='company-segmento-title'), 
            html.H2(id='company-title'),
            # Your content here...
            dcc.Graph(id='graph-ativos'),
        ]
    )
])

@app.callback(
    [Output('company-segmento-title', 'children'),
     Output('company-title', 'children'),
     Output('company-df', 'data')],  # Added output to store df
    [Input('store-selected-company', 'data'),
     Input('store-selected-setor', 'data'),
     Input('store-selected-subsetor', 'data'),
     Input('store-selected-segmento', 'data')]
)
def update_titles(stored_company, stored_setor, stored_subsetor, stored_segmento):
    # If any of the stored data is None, prevent the update
    if None in [stored_company]:
        raise exceptions.PreventUpdate
    
    # Extract the stored values
    companhia = stored_company.get('company', '')
    setor = stored_setor.get('setor', '')
    subsetor = stored_subsetor.get('subsetor', '')
    segmento = stored_segmento.get('segmento', '')
    
    # Construct the titles
    # Load the DataFrame when a company is selected
    df = pd.DataFrame()
    if companhia:
        # Construct the path to the file
        file = os.path.join(f'{b3.app_folder}company/{companhia}')
        
        # Check if the file exists
        if os.path.exists(file+'.pkl'):
            # Load the DataFrame
            df = run.load_pkl(file)
            # Now df contains the data and can be used for further processing
            print(len(df), companhia)
        else:
            print(f"No data file found for company: {companhia}")

        segmento_title = f"{setor} - {subsetor} - {segmento}"
        company_title = companhia
    else:
        segmento_title = ''
        company_title = ''

    # stored_df = df.to_dict(orient='records')
    # Compress and encode data
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode='w') as f:
        df.to_parquet(f)
    compressed_data = base64.b64encode(buffer.getvalue()).decode('utf-8')


    return segmento_title, company_title, compressed_data
