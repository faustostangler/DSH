from dash import html, dcc, exceptions
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

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

from num2words import num2words

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
graphs_1_components = []
for i, (line, info) in enumerate(graphs_1.items()):
    graphs_1_components.extend([
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
            html.Div(id='company-info'),
            # Additional components like graphs, tables, etc.
            *graphs_1_components,
            html.Hr(),
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

@app.callback(
    Output('company-info', 'children'),
    [Input('company-df', 'data')]
)
def update_company_info(compressed_data):
    """
    Generate a section of components that display company information.

    Parameters:
    - df (pd.DataFrame): DataFrame containing company information.

    Returns:
    - list: List of components to be added to the layout.
    """
    # Ensure compressed_data is string and not None or other type
    if not isinstance(compressed_data, str):
        print('gotcha')
        raise exceptions.PreventUpdate("Data is not valid")

    df = decompress_data(compressed_data)
    # Extract information from DataFrame and generate components
    company_name = df.iloc[0]['DENOM_CIA'] if not df.empty else ''
    atividade = df.iloc[0]['ATIVIDADE'] if not df.empty else ''
    listagem = df.iloc[0]['LISTAGEM'] if not df.empty else ''
    cnpj = df.iloc[0]['CNPJ_CIA'] if not df.empty else ''
    data_min, data_max = df['DT_REFER'].min().strftime("%d/%m/%Y"), df['DT_REFER'].max().strftime("%d/%m/%Y")
    site = df.iloc[0]['SITE'] if not df.empty else ''
    escriturador = df.iloc[0]['ESCRITURADOR'] if not df.empty else ''
    acoes_on = df.iloc[-1]['00.01.01 - Ações ON'] if not df.empty else ''
    acoes_pn = df.iloc[-1]['00.02.01 - Ações PN'] if not df.empty else ''
    ativo_total = df.iloc[-1]['01 - Ativo Total'] if not df.empty else ''
    acoes_on_words = num2words(acoes_on, lang='pt_BR')
    acoes_pn_words = num2words(acoes_pn, lang='pt_BR') if not np.isnan(acoes_pn) else 'N/A'
    ativo_total_words = num2words(ativo_total, lang='pt_BR')
    acoes_on = "{:,.0f}".format(acoes_on).replace(",", "X").replace(".", ",").replace("X", ".")
    acoes_pn = "{:,.0f}".format(acoes_pn).replace(",", "X").replace(".", ",").replace("X", ".") if not np.isnan(acoes_pn) else 'N/A'
    ativo_total = "{:,.0f}".format(ativo_total).replace(",", "X").replace(".", ",").replace("X", ".")

    header_1 = [
        html.H4(f"{company_name}", id='company-name-info'),
        ]
    body_1 = [
        html.P(f"{atividade}", id='atividade-info'),
    ]
    footer_1 = [
        dbc.Row(
            [
                dbc.Col(html.P(f"CNPJ: {cnpj}", id='cnpj-info'), width=6),
                dbc.Col(html.P(f"Listagem: {listagem}", id='listagem-info'), width=6)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.P(f"Site: {site}", id='site-info'), width=6),
                dbc.Col(html.P(f"Escriturador: {escriturador}", id='escriturador-info'), width=6)
            ]
        ), 
    ]

    header_2 = [
        html.H4(f'Últimos Dados'),
        ]
    body_2 = [
        html.P(["Ações ON: ", html.Strong(f"{acoes_on}"),  f" ações ({acoes_on_words})"], id='acoes_on-info'),
        html.P(["Ações PN: ", html.Strong(f"{acoes_pn}"),  f" ações ({acoes_on_words})"], id='acoes_on-info'),
        html.P(["Ativo Total: R$: ", html.Strong(f"{ativo_total}"),  f" ações ({ativo_total_words})"], id='ativo_total-info'),
    ]
    footer_2 = [
        html.P(f"Dados disponíveis de {data_min} até {data_max}", id='data-info'),
    ]

    card_1 = dbc.Card([
        dbc.CardHeader(header_1), 
        dbc.CardBody(body_1), 
        dbc.CardFooter(footer_1), 
        ])
    card_2 = dbc.Card([
        dbc.CardHeader(header_2), 
        dbc.CardBody(body_2), 
        dbc.CardFooter(footer_2), 
        ])

    return html.Div([card_1, html.P(), card_2, html.P()])

