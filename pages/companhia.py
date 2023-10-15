# Importing necessary modules and libraries
from dash import html, dcc, exceptions
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
from assets.graphs import graphs_0, graphs_1

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

# Generates a callback for updating graphs based on a line number, unit, and info.
def generate_callback(g, p, title, info):
    @app.callback(
        Output(f'graph_{g}_{p}', 'figure'),
        [Input('company-df', 'data')]
    )
    def update_graph(compressed_data):
        # Ensure compressed_data is string and not None or other type
        if not isinstance(compressed_data, str):
            raise exceptions.PreventUpdate("Data is not valid")

        # Decompressing the data
        df = decompress_data(compressed_data)
        
        # Debugging log
        tickers = np.sort(df['TICKER'].unique())
        df_ticker = ticker = []
        for ticker in tickers:
            df_ticker.append(df[df['TICKER'] == ticker])
        df = df_ticker[0]
        print(f'{ticker} Debugging log - df[0] attention please {tickers}')

        # Updating the graph
        plot_info = {
            'plot_title': title,  # Using the dict key as plot title
            'data': info['data'],
            'options': info['options']
        }
        fig = run.plot_tweak(df, plot_info)
        return fig

    return update_graph

def generate_collapse_callbacks(n_groups):
    """
    Generate callbacks to manage the collapse components for each graph group.
    
    Parameters:
    - n_groups (int): The number of graph groups.
    """
    for g in range(n_groups):
        @app.callback(
            Output(f"collapse-{g}", "is_open"),
            [Input(f"btn-{g}", "n_clicks")],
            [State(f"collapse-{g}", "is_open")]
        )
        def toggle_collapse(n, is_open, g=g):  # Use default arg to remember the loop variable
            if n:
                return not is_open
            return is_open

def create_layout_from_plots(all_plots):
    """
    Create layout components from a dictionary of plots.

    Parameters:
    - all_plots (dict): Dictionary containing plot components.

    Returns:
    - list: List of components to be added to the layout.
    """
    layout_components = []
    try:
        for g, plots in all_plots.items():
           # Append each plot (which is a dbc.Card component) directly to layout_components
            layout_components.append(
                dbc.Button(
                    f"Toggle Graph Group {g}", 
                    id=f"btn-{g}", 
                    className="mb-3", 
                    color="primary"
                )
            )

            # Add a line break for spacing
            layout_components.append(html.Br())

            # Collapsible section containing the graph group
            layout_components.append(
                dbc.Collapse(
                    plots, 
                    id=f"collapse-{g}", 
                    is_open=True  # Setting this to True will make it visible at start
                )
            )
    except Exception as e:
        print(f"Error creating layout: {str(e)}")
        # You might want to return a placeholder or error message in the layout in case of error
        layout_components.append(html.P("Error loading plots."))
        
    return layout_components

# ----- CODE LOGIC -----
# Define units as a list of graphs
groups_of_graph = [graphs_0, graphs_1]
all_plots = {}

# Loop through each unit (graph) and generate callbacks and components
for g, graph in enumerate(groups_of_graph):
    current_graph_components = []
    for p, (title, info) in enumerate(graph.items()):
        # Generating callbacks using lines from the current graph
        generate_callback(g, p, title, info)  # Passing title and info to callback generator

        # Creating a dbc.Card component for each graph and appending it to current_graph_components
        current_graph_components.append(
            dbc.Card([
                dbc.CardHeader([
                    html.H5(title, id=f'graph_{g}_{p}_title'),  # Using title as H5 content
                ]), 
                dbc.CardBody([
                    html.P(info['info']['description'], id=f'graph_{g}_{p}_info'), 
                    dcc.Graph(id=f'graph_{g}_{p}'), 
                ]),
                dbc.CardFooter([
                    html.P(f"Footer for {title}", id=f'graph_{g}_{p}_footer'), 
                    ]),  # footer
            # html.Hr(), 
            ]), 
        )
        # Add a line break for spacing
        current_graph_components.append(html.Br())

    # Storing the created components in the dictionary using the unit index as the key
    all_plots[g] = current_graph_components

generate_collapse_callbacks(len(all_plots))

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

            # Include dynamically generated graph components in the layout
            *create_layout_from_plots(all_plots), 
            # More contents here...
        ]
    )
])

# ----- CALLBACKS -----

# Callback to update titles and load company data
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

# Callback to update company information
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
    return html.Div([layout_row])


