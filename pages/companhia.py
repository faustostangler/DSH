# Importing necessary modules and libraries
import dash
from dash import html, dcc, exceptions
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc

from app import app
from assets.graphs import construct_graphs

import assets.helper as b3
import assets.functions as run

import os
import pandas as pd
import numpy as np
import plotly.express as px
import gzip
import io
import base64

# ----- FUNCTIONS -----
# Decompresses data and returns it as a DataFrame.
def decompress_data(compressed_data):
    """
    Decompress and decode the provided data.

    Parameters:
    - compressed_data (str): Compressed and encoded data.

    Returns:
    - pd.DataFrame: Decompressed and decoded data as a DataFrame.
    """
    # Creating a buffer to hold compressed data and decompressing the data
    buffer = io.BytesIO(base64.b64decode(compressed_data))
    with gzip.GzipFile(fileobj=buffer, mode='r') as f:
        df = pd.read_parquet(f)
    return df

def extract_company_info(df):
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
    patrimonio = df.iloc[-1]['02.03 - Patrimônio Líquido'] if not df.empty else ''
    lucro = df.iloc[-1]['03.11 - Lucro Líquido'] if not df.empty else ''
    divida = df.iloc[-1]['12.01.02 - Dívida Bruta'] if not df.empty else ''
    roe = df.iloc[-1]['14.04.01 - ROE (Resultado por Patrimônio)'] if not df.empty else ''
    preco = df.iloc[-1]['Adj Close'] if not df.empty else ''

    header_1 = [
        html.H4([
            html.A(f"{company_name}", href=f"https://www.google.com/search?q=RI+{company_name.replace(' ', '+')}", target='_blank', id='company-name-info')
        ]),
        ]
    body_1 = [
        html.P(f"{atividade}", id='atividade-info'),
    ]
    footer_1 = [
        dbc.Row(
            [
                dbc.Col(html.P(["CNPJ: ", html.A(f"{cnpj}", href=f"https://cnpj.biz/{''.join(filter(str.isdigit, cnpj))}", target='_blank', id='cnpj-link')]), width=6), 
                dbc.Col(html.P(f"Listagem: {listagem}", id='listagem-info'), width=6)
            ]
        ),
        dbc.Row(
            [
                

                dbc.Col(html.P(html.P(["Site: ", html.A(site, href=site, target='_blank', id='site-link')])), width=6),
                dbc.Col(html.P(f"Escriturador: {escriturador}", id='escriturador-info'), width=6)
            ]
        ), 
    ]

    header_2 = [
        html.H4(f'ÚLTIMOS DADOS'),
        ]
    body_2 = [
        html.P(["Ações ON: ", html.Strong("{:,.0f}".format(acoes_on).replace(',', '.')),  f" ações"], id='acoes_on-info'),
        html.P(["Ações PN: ", html.Strong("{:,.0f}".format(acoes_pn).replace(',', '.')),  f" ações"], id='acoes_on-info'),
        html.Hr(), 
        html.P(["Ativo Total: R$: ", html.Strong("{:,.0f}".format(ativo_total).replace(',', '.')), ], id='ativo_total-info'),
        html.P(["Patrimônio: R$: ", html.Strong("{:,.0f}".format(patrimonio).replace(',', '.')), ], id='patrimonio-info'),
        html.P(["Lucro Líquido: R$: ", html.Strong("{:,.0f}".format(lucro).replace(',', '.')), ], id='lucro-info'),
        html.P(["Dívida Bruta: R$: ", html.Strong("{:,.0f}".format(divida).replace(',', '.')), ], id='divida-info'),
        html.P(["ROE: ", html.Strong("{:,.2f}".format(roe*100).replace(",", "X").replace(".", ",").replace("X", ".")), "%"], id='roe-info'),
        html.Hr(), 
        html.P(["Preço por Ação: R$: ", html.Strong("{:,.2f}".format(preco).replace(",", "X").replace(".", ",").replace("X", ".")), ], id='preco-info'),
        html.P(["Valor de Mercado: R$: ", html.Strong("{:,.0f}".format(preco*(acoes_on)).replace(",", "X").replace(".", ",").replace("X", ".")), ], id='preco-info'),


    ]
    footer_2 = [
        html.P(f"Dados disponíveis de {data_min} até {data_max}", id='data-info'),
    ]

    # Creating a card to display company information (card 1)
    card_1 = dbc.Card([
        dbc.CardHeader(header_1), 
        dbc.CardBody(body_1), 
        dbc.CardFooter(footer_1)
    ])

    # Creating a card to display company information (card 2)
    card_2 = dbc.Card([
        dbc.CardHeader(header_2), 
        dbc.CardBody(body_2), 
        dbc.CardFooter(footer_2)
    ])

    # Creating a row with two columns to hold card_1 and card_2 side by side
    layout_row = dbc.Row([
        dbc.Col(card_1, width=6),  # card_1 occupies half of the row
        dbc.Col(card_2, width=6)   # card_2 occupies the other half
    ])

    # Returning a Div that contains the layout row
    company_info = html.Div([layout_row])

    # Return the constructed layout
    return company_info

def generate_button_and_content(group_index, content_list):
    button =  [
        dbc.Button(
            f"Mostrar Gráficos", 
            id={'type': 'toggle-button', 'index': group_index}, 
            className="mb-2"
        ),
        html.Br(), 
        dbc.Collapse(
            content_list, 
            id={'type': 'collapse-content', 'index': group_index},
            is_open=False
        )
    ]
    return button

# ----- CODE LOGIC -----


# ----- LAYOUT -----
layout = html.Div([
    # Storing data to be passed between callbacks
    dcc.Store(id='company-df', storage_type='session'), 
    dcc.Store(id='store-graphs-manual', storage_type='session'), 

    # Loading spinner that appears while callbacks are performed
    dcc.Loading(
        id="loading",
        type="default", # default, circle, cube, dot
        style={"position": "fixed", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)"},
        children=[
            # Main titles of the page 
            html.H1("Análise Fundamentalista", id='title'),
            html.H2(id='company-segmento-title'), 
            html.H2(id='company-title'),
            html.Div(id='company-info'),
            html.Div(id='company-plots'),
            # More contents here...
        ]
    )
])


# ----- CALLBACKS -----
@app.callback(
    [
        Output('company-segmento-title', 'children'),
        Output('company-title', 'children'),
        Output('company-df', 'data'), 
        Output('store-graphs-manual', 'data')
    ],  
    [
        Input('store-selected-company', 'data'),
        Input('store-selected-setor', 'data'),
        Input('store-selected-subsetor', 'data'),
        Input('store-selected-segmento', 'data'), 
    ], 
)
def update_company(stored_company, stored_setor, stored_subsetor, stored_segmento):
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
    setor = stored_setor.get('setor', '')
    subsetor = stored_subsetor.get('subsetor', '')
    segmento = stored_segmento.get('segmento', '')
    companhia = stored_company.get('company', '')

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

    # Generate graphs_manual
    graphs_manual = construct_graphs(df)

    # Compress and encode data for efficient storage
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode='w') as f:
        df.to_parquet(f)
    compressed_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return segmento_title, company_title, compressed_data, graphs_manual


@app.callback(
    [
        Output('company-info', 'children'),
        Output('company-plots', 'children'),
    ], 
    [
        Input('company-df', 'data'), 
    ]
)
def update_company_info(compressed_data):
    # Decompress the data
    df = decompress_data(compressed_data)
    # If df is empty, return an error message
    if df.empty:
        return html.P("No company data available.")

    # Get Company Info
    company_info = extract_company_info(df)

    graphs_manual = construct_graphs(df)

    blocks = []
    for g, (group_key, group) in enumerate(graphs_manual.items()):
        titles = []
        for l, (line_key, line) in enumerate(group.items()):
            for p, (plot_key, plot_info) in enumerate(line.items()):
                title = plot_info['info']['title']
                titles.append(html.P(f'g {g} l {l} p {p} {plot_info}'))
        blocks.extend(generate_button_and_content(g, titles))  # Use extend, not append

    return company_info, blocks


@app.callback(
    Output({'type': 'collapse-content', 'index': ALL}, 'is_open'),
    Input({'type': 'toggle-button', 'index': ALL}, 'n_clicks'),
    State({'type': 'collapse-content', 'index': ALL}, 'is_open'),
    prevent_initial_call=True
)
def toggle_content_visibility(n_clicks, is_open_states):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    group_index = eval(button_id)['index']

    # Toggle the is_open state for the clicked button's collapse
    is_open_states[group_index] = not is_open_states[group_index]
    return is_open_states
