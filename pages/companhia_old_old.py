# Importing necessary modules and libraries
from dash import html, dcc, exceptions
from dash.dependencies import Input, Output, State
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

# Generates a callback for updating graphs based on a line number, unit, and info.
def create_callback(g, l, p, info):
    print(f"Creating callback for graph_{g}_{l}_{p}")
    @app.callback(
        Output(f'graph_{g}_{l}_{p}', 'figure'),
        [Input('company-df', 'data')]
    )
    def inner_update_graph(compressed_data):
        print("Callback triggered!")
        raise exceptions.PreventUpdate
    
    return inner_update_graph

# def generate_collapse_callbacks(n_groups):
#     """
#     Generate callbacks to manage the collapse components for each graph group.
    
#     Parameters:
#     - n_groups (int): The number of graph groups.
#     """
#     for g in range(n_groups):
#         @app.callback(
#             Output(f"collapse-{g}", "is_open"),
#             [Input(f"btn-{g}", "n_clicks")],
#             [State(f"collapse-{g}", "is_open")]
#         )
#         def toggle_collapse(n, is_open, g=g):  # Use default arg to remember the loop variable
#             if n:
#                 return not is_open
#             return is_open

def create_layout_from_plots(all_plots, df):
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
                    f"Ocultar Seção", 
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

# # ----- CODE LOGIC -----
# # groups_of_graph = [graphs_0, graphs_1]
# groups_of_graph = {}
# # for key, value in graphs_default.items():
# #     groups_of_graph[key] = value
# for key, value in graphs_manual.items():
#     groups_of_graph[f'{key}_manual'] = value
# groups_of_graph = {f"{key}_manual": value for key, value in graphs_manual.items()}

# all_plots = {}

# # Loop through each unit (graph) and generate callbacks and components
# for g, (key, group) in enumerate(groups_of_graph.items()):
#     current_graph_components = []
#     for l, (line_number, line_content) in enumerate(group.items()):
#         for p, (plot_type, info) in enumerate(line_content.items()):
#             # Generating callbacks using lines from the current graph
#             generate_callback(g, l, p, info)

#             # Creating a dbc.Card component for each graph and appending it to current_graph_components
#             current_graph_components.append(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.H5(info['info']['title'], id=f'graph_{g}_{l}_{p}_title'),
#                     ]),
#                     dbc.CardBody([
#                         html.P(info['info']['description'], id=f'graph_{g}_{l}_{p}_info'),
#                         dcc.Graph(id=f'graph_{g}_{l}_{p}'),
#                     ]),
#                     dbc.CardFooter([
#                         html.P(f"Footer for {info['info']['title']}", id=f'graph_{g}_{l}_{p}_footer'),
#                     ]),
#                 ]),
#             )
#             # Add a line break for spacing
#             current_graph_components.append(html.Br())

#     # Storing the created components in the dictionary using the group index as the key
#     all_plots[g] = current_graph_components

# generate_collapse_callbacks(len(all_plots))

# ----- LAYOUT -----
layout = html.Div([
    # Storing data to be passed between callbacks
    dcc.Store(id='company-df', storage_type='session'), 

    # Loading spinner that appears while callbacks are performed
    dcc.Loading(
        id="loading",
        type="default", # default, circle, cube, dot
        style={"position": "fixed", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)"},
        children=[
            # Main titles of the page 
            html.H1("Análise Fundamentalista"),
            html.H2(id='company-segmento-title'), 
            html.H2(id='company-title'),
            html.Div(id='company-info'),
            html.Div(id='plot-container'),  
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
        Output('company-df', 'data'), 
    ],  
    [
        Input('store-selected-company', 'data'),
        Input('store-selected-setor', 'data'),
        Input('store-selected-subsetor', 'data'),
        Input('store-selected-segmento', 'data'), 
    ], 
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
        file = os.path.join(f'{b3.app_folder}/company/{companhia}')
        
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
    Output('plot-container', 'children'),
    [Input('company-df', 'data')]
)
def update_layout(compressed_data):
    if not isinstance(compressed_data, str):
        raise exceptions.PreventUpdate("Data is not valid")

    # load data
    df = decompress_data(compressed_data)

    # Call the function with df_columns
    graphs_manual = construct_graphs(df)

    groups_of_graph = {f"{key}_manual": value for key, value in graphs_manual.items()}
    # print('bbb', groups_of_graph)

    all_plots = {}
    
    # Loop through each unit (graph) and generate callbacks and components
    for g, (key, group) in enumerate(graphs_manual.items()):
        current_graph_components = []
        for l, (line_number, line_content) in enumerate(group.items()):
            for p, (plot_type, info) in enumerate(line_content.items()):
                # Create Callbacks for each plot
                create_callback(g, l, p, info)

                # Creating a dbc.Card component for each graph and appending it to current_graph_components
                # THEN HELP ME HERE
                current_graph_components.append(
                    dbc.Card([
                        dbc.CardHeader([
                            html.H5(info['info']['title'], id=f'graph_{g}_{l}_{p}_title'),
                        ]),
                        dbc.CardBody([
                            html.P(info['info']['description'], id=f'graph_{g}_{l}_{p}_info'),
                            dcc.Graph(id=f'graph_{g}_{l}_{p}'),
                        ]),
                        dbc.CardFooter([
                            html.P(f"g {g}, l {l}, p {p}, info {info} -- Footer for {info['info']['title']}", id=f'graph_{g}_{l}_{p}_footer'),
                        ]),
                    ]),
                )
                # Add a line break for spacing
                current_graph_components.append(html.Br())

        # Storing the created components in the dictionary using the group index as the key
        all_plots[g] = current_graph_components
    
    return create_layout_from_plots(all_plots, df)
