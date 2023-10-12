import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app

import threading
import time

import assets.helper as b3
import assets.functions as run

import pandas as pd

# Sidebar layout
layout = html.Div([
    # store data
    dcc.Store(id='store-data', storage_type='session'), 

    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0,
        max_intervals=1  # stops the interval after 1 update
    ), 

    # Dropdown for 'Setor' selection
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='dropdown-setor', 
                options=[],  
                value=None,  
                placeholder='Select a Setor'  
            ), 
            width={"size": 10, "offset": 1}  
        ),
    ]),

    # Dropdown for 'Subsetor' selection
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='dropdown-subsetor', 
                options=[],  
                value=None,  
                placeholder='Select a Subsetor'
            ), 
            width={"size": 10, "offset": 1},
            id='col-subsetor'  
        ),
    ]),

    # Dropdown for 'Segmento' selection
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='dropdown-segmento', 
                options=[],  
                value=None,  
                placeholder='Select a Segmento'
            ), 
            width={"size": 10, "offset": 1},
            id='col-segmento'  
        ),
    ]),
    
    # Dropdown for 'COMPANY' (PREGAO) selection
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='dropdown-company', 
                options=[],  
                value=None,  
                placeholder='Select a Company'
            ), 
            width={"size": 10, "offset": 1},
            id='col-company'  
        ),
    ]),
    
])
layout.children.extend([
    # Multiselect Dropdown for 'Other Companies' (PREGAO) selection
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='multiselect-company', 
                options=[],  
                value=[],  
                placeholder='Select Other Companies',
                multi=True  # Enable multiselect
            ), 
            width={"size": 10, "offset": 1},
            id='col-multiselect-company'
        ),
    ]),
    
    # Display selected other companies
    dbc.Row([
        dbc.Col(
            html.H4(id='display-other-companies'),
            width={"size": 10, "offset": 1}
        )
    ])
])
# callbacks

# Load data, store it, and populate the 'Setor' dropdown
@app.callback(
    [Output('store-data', 'data'),
     Output('dropdown-setor', 'options')],
    Input('interval-component', 'n_intervals')
)
def load_data(_):
    df = run.load_pkl('sss')  # Your data loading function here
    
    stored_data = df.to_dict(orient='records')
    
    dropdown_options = [{'label': setor, 'value': setor} for setor in df['SETOR'].sort_values().unique()]
    
    return stored_data, dropdown_options

# @app.callback(
#     Output('store-selected-setor', 'data'),
#     Input('dropdown-setor', 'value')
# )
# def store_selected_setor(selected_setor):
#     return {'setor': selected_setor}

# Toggle visibility and reset 'Subsetor' dropdown when 'Setor' is selected
@app.callback(
    [Output('dropdown-subsetor', 'value'),
     Output('col-subsetor', 'style')],
    Input('dropdown-setor', 'value')
)
def manage_subsetor_on_setor_change(selected_setor):
    if selected_setor is None:
        return None, {'display': 'none'}
    else:
        return None, {'display': 'block'}

# Update 'Subsetor' options when 'Setor' is selected
@app.callback(
    Output('dropdown-subsetor', 'options'),
    [Input('dropdown-setor', 'value'),
     Input('store-data', 'data')]
)
def update_subsetor_options(selected_setor, stored_data):
    if selected_setor is None or stored_data is None:
        raise dash.exceptions.PreventUpdate
    
    df = pd.DataFrame(stored_data)
    filtered_df = df[df['SETOR'] == selected_setor]
    
    subsetor_options = [{'label': subsetor, 'value': subsetor} for subsetor in filtered_df['SUBSETOR'].sort_values().unique()]
    
    return subsetor_options

# @app.callback(
#     Output('store-selected-subsetor', 'data'),
#     Input('dropdown-subsetor', 'value')
# )
# def store_selected_subsetor(selected_subsetor):
#     return {'subsetor': selected_subsetor}


# Toggle visibility and reset 'Segmento' dropdown when 'Subsetor' is selected
@app.callback(
    [Output('dropdown-segmento', 'value'),
     Output('col-segmento', 'style')],
    Input('dropdown-subsetor', 'value')
)
def manage_segmento_on_subsetor_change(selected_subsetor):
    if selected_subsetor is None:
        return None, {'display': 'none'}
    else:
        return None, {'display': 'block'}

# Update 'Segmento' options when 'Subsetor' is selected
@app.callback(
    Output('dropdown-segmento', 'options'),
    [Input('dropdown-subsetor', 'value'),
     Input('store-data', 'data')]
)
def update_segmento_options(selected_subsetor, stored_data):
    if selected_subsetor is None or stored_data is None:
        raise dash.exceptions.PreventUpdate
    
    df = pd.DataFrame(stored_data)
    filtered_df = df[df['SUBSETOR'] == selected_subsetor]
    
    segmento_options = [{'label': segmento, 'value': segmento} for segmento in filtered_df['SEGMENTO'].sort_values().unique()]
    
    return segmento_options

# @app.callback(
#     [Output('store-selected-setor', 'data'),
#      Output('store-selected-segmento', 'data')],
#     [Input('dropdown-setor', 'value'),
#      Input('dropdown-segmento', 'value')]
# )
# def store_selected_values(selected_setor, selected_segmento):
#     return {'setor': selected_setor}, {'segmento': selected_segmento}


@app.callback(
    [Output('dropdown-company', 'value'),
     Output('col-company', 'style')],
    Input('dropdown-segmento', 'value')
)
def manage_company_on_segmento_change(selected_segmento):
    if selected_segmento is None:
        return None, {'display': 'none'}
    else:
        return None, {'display': 'block'}

@app.callback(
    Output('dropdown-company', 'options'),
    [Input('dropdown-segmento', 'value'),
     Input('store-data', 'data')]
)
def update_company_options(selected_segmento, stored_data):
    if selected_segmento is None or stored_data is None:
        raise dash.exceptions.PreventUpdate
    
    df = pd.DataFrame(stored_data)
    filtered_df = df[df['SEGMENTO'] == selected_segmento]
    
    company_options = [{'label': company, 'value': company} for company in filtered_df['PREGAO'].sort_values().unique()]
    
    return company_options

# Toggle visibility and update 'Other Companies' options when 'COMPANY' is selected
@app.callback(
    [Output('multiselect-company', 'value'),
     Output('col-multiselect-company', 'style'),
     Output('multiselect-company', 'options')],
    [Input('dropdown-company', 'value'),
     Input('store-data', 'data')]
)
def manage_other_companies_on_company_change(selected_company, stored_data):
    if selected_company is None or stored_data is None:
        return [], {'display': 'none'}, []

    df = pd.DataFrame(stored_data)
    
    # Exclude the selected company
    other_companies = df[df['PREGAO'] != selected_company]['PREGAO'].sort_values().unique()
    other_company_options = [{'label': company, 'value': company} for company in other_companies]
    
    return [], {'display': 'block'}, other_company_options

# Display selected other companies
@app.callback(
    Output('display-other-companies', 'children'),
    Input('multiselect-company', 'value')
)
def display_selected_other_companies(selected_other_companies):
    if not selected_other_companies:
        return ""
    else:
        return f"Comparar com: {', '.join(selected_other_companies)}"

# @app.callback(
#     Output('url', 'pathname'),
#     [Input('dropdown-setor', 'value'),
#      Input('dropdown-subsetor', 'value'),
#      Input('dropdown-segmento', 'value')]
# )
# def update_url_path(selected_setor, selected_subsetor, selected_segmento):
#     # If a segment is selected, navigate to the segment page.
#     if selected_segmento is not None:
#         return '/segmento'
#     # If a subsetor is selected (and no segment), navigate to the subsetor page.
#     elif selected_subsetor is not None:
#         return '/subsetor'
#     # If a setor is selected (and no subsetor or segment), navigate to the setor page.
#     elif selected_setor is not None:
#         return '/setor'
#     # If nothing is selected, navigate to the home.
#     else:
#         return '/home'
# @app.callback(
#     [Output('store-selected-setor', 'data'),
#      Output('store-selected-subsetor', 'data'),
#      Output('url', 'pathname')],
#     [Input('dropdown-setor', 'value'),
#      Input('dropdown-subsetor', 'value'),
#      Input('dropdown-segmento', 'value')]
# )
# def update_stores_and_url(selected_setor, selected_subsetor, selected_segmento):
#     stored_setor = {'setor': selected_setor}
#     stored_subsetor = {'subsetor': selected_subsetor}
    
#     # Update URL
#     if selected_segmento is not None:
#         new_pathname = '/segmento'
#     elif selected_subsetor is not None:
#         new_pathname = '/subsetor'
#     elif selected_setor is not None:
#         new_pathname = '/setor'
#     else:
#         new_pathname = '/home'
    
#     return stored_setor, stored_subsetor, new_pathname

# In the callbacks of sidebar.py
@app.callback(
    [Output('store-selected-setor', 'data'),
     Output('store-selected-subsetor', 'data'),
     Output('store-selected-segmento', 'data'),
     Output('store-selected-company', 'data'),
     Output('url', 'pathname')],
    [Input('dropdown-setor', 'value'),
     Input('dropdown-subsetor', 'value'),
     Input('dropdown-segmento', 'value'),
     Input('dropdown-company', 'value')]
)
def update_stores_and_url(selected_setor, selected_subsetor, selected_segmento, selected_company):
    stored_setor = {'setor': selected_setor}
    stored_subsetor = {'subsetor': selected_subsetor}
    stored_segmento = {'segmento': selected_segmento}
    stored_company = {'company': selected_company}
    
    # Update URL
    if selected_company is not None:
        new_pathname = '/companhia'
    elif selected_segmento is not None:
        new_pathname = '/segmento'
    elif selected_subsetor is not None:
        new_pathname = '/subsetor'
    elif selected_setor is not None:
        new_pathname = '/setor'
    else:
        new_pathname = '/home'
    
    return stored_setor, stored_subsetor, stored_segmento, stored_company, new_pathname
