import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

from app import app  # Importing the app from another module

# Importing additional modules for threading and custom functions
import threading
import time
import assets.helper as b3
import assets.functions as run

# ----- LAYOUT -----
# Defining the sidebar layout with multiple dropdowns and a data storage component
layout = html.Div([
    # A dcc.Store component for storing the data used throughout the app
    dcc.Store(id='store-data', storage_type='session'), 

    # An interval component to trigger data loading at a regular interval
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0,
        max_intervals=1  # stops the interval after 1 update
    ), 
    # A series of dropdowns for selecting 'Setor', 'Subsetor', 'Segmento', and 'Company' (PREGAO)
    dbc.Row([dbc.Col(dcc.Dropdown(id='dropdown-setor', options=[], value=None, placeholder='Select a Setor'), width={"size": 10, "offset": 1})]),
    dbc.Row([dbc.Col(dcc.Dropdown(id='dropdown-subsetor', options=[], value=None, placeholder='Select a Subsetor'), width={"size": 10, "offset": 1}, id='col-subsetor')]),
    dbc.Row([dbc.Col(dcc.Dropdown(id='dropdown-segmento', options=[], value=None, placeholder='Select a Segmento'), width={"size": 10, "offset": 1}, id='col-segmento')]),
    dbc.Row([dbc.Col(dcc.Dropdown(id='dropdown-company', options=[], value=None, placeholder='Select a Company'), width={"size": 10, "offset": 1}, id='col-company')]),

    # Additional dropdown for multi-selection of other companies
    dbc.Row([dbc.Col(dcc.Dropdown(id='multiselect-company', options=[], value=[], placeholder='Select Other Companies', multi=True), width={"size": 10, "offset": 1}, id='col-multiselect-company')]),

    # Display area for selected other companies
    dbc.Row([dbc.Col(html.H4(id='display-other-companies'), width={"size": 10, "offset": 1})])
])

# ----- CALLBACKS -----
# Callback 1: Load data and populate 'Setor' dropdown
@app.callback(
    [Output('store-data', 'data'),
     Output('dropdown-setor', 'options')],
    Input('interval-component', 'n_intervals')
)
def load_data(_):
    """
    Load the dataframe, store it in a dcc.Store, and populate the 'Setor' dropdown.
    Triggered by the interval-component, it fetches and processes the data once.
    """
    # Load data
    df = run.sys_load_pkl(f'{b3.app_folder}/sss')

    # Store data in a format suitable for dcc.Store
    stored_data = df.to_dict(orient='records')
    
    # Create options for the 'Setor' dropdown
    dropdown_options = [{'label': setor, 'value': setor} for setor in df['SETOR'].sort_values().unique()]
    
    return stored_data, dropdown_options

# Callback 2: Manage 'Subsetor' dropdown visibility and reset its value upon 'Setor' selection
@app.callback(
    [Output('dropdown-subsetor', 'value'),
     Output('col-subsetor', 'style')],
    Input('dropdown-setor', 'value')
)
def manage_subsetor_on_setor_change(selected_setor):
    """
    Manage the visibility and value reset of the 'Subsetor' dropdown based on the selected 'Setor'.
    If a 'Setor' is selected, the 'Subsetor' dropdown becomes visible and its value is reset.
    """
    if selected_setor is None:
        return None, {'display': 'none'}
    else:
        return None, {'display': 'block'}

# Callback 3: Update 'Subsetor' dropdown options based on 'Setor' selection
@app.callback(
    Output('dropdown-subsetor', 'options'),
    [Input('dropdown-setor', 'value'),
     Input('store-data', 'data')]
)
def update_subsetor_options(selected_setor, stored_data):
    """
    Update the options of the 'Subsetor' dropdown based on the selected 'Setor'.
    It fetches the relevant subsetors by filtering the stored data.
    """
    if selected_setor is None or stored_data is None:
        raise dash.exceptions.PreventUpdate
    
    df = pd.DataFrame(stored_data)
    filtered_df = df[df['SETOR'] == selected_setor]
    
    subsetor_options = [{'label': subsetor, 'value': subsetor} for subsetor in filtered_df['SUBSETOR'].sort_values().unique()]
    
    return subsetor_options

# Callback 4: Manage 'Segmento' dropdown visibility and reset its value upon 'Subsetor' selection
@app.callback(
    [Output('dropdown-segmento', 'value'),
     Output('col-segmento', 'style')],
    Input('dropdown-subsetor', 'value')
)
def manage_segmento_on_subsetor_change(selected_subsetor):
    """
    Manage the visibility and value reset of the 'Segmento' dropdown based on the selected 'Subsetor'.
    """
    if selected_subsetor is None:
        return None, {'display': 'none'}
    else:
        return None, {'display': 'block'}

# Callback 5: Update 'Segmento' dropdown options based on 'Subsetor' selection
@app.callback(
    Output('dropdown-segmento', 'options'),
    [Input('dropdown-setor', 'value'),
     Input('dropdown-subsetor', 'value'),
     Input('store-data', 'data')]
)
def update_segmento_options(selected_setor, selected_subsetor, stored_data):
    """
    Update the options of the 'Segmento' dropdown based on the selected 'Subsetor'.
    """
    if selected_setor is None or selected_subsetor is None or stored_data is None:
        raise dash.exceptions.PreventUpdate
    
    df = pd.DataFrame(stored_data)
    filtered_df = df[(df['SETOR'] == selected_setor) & (df['SUBSETOR'] == selected_subsetor)]
    
    segmento_options = [{'label': segmento, 'value': segmento} for segmento in filtered_df['SEGMENTO'].sort_values().unique()]
    
    return segmento_options

# Callback 6: Manage 'Company' dropdown visibility and reset its value upon 'Segmento' selection
@app.callback(
    [Output('dropdown-company', 'value'),
     Output('col-company', 'style')],
    Input('dropdown-segmento', 'value')
)
def manage_company_on_segmento_change(selected_segmento):
    """
    Manage the visibility and value reset of the 'Company' dropdown based on the selected 'Segmento'.
    """
    if selected_segmento is None:
        return None, {'display': 'none'}
    else:
        return None, {'display': 'block'}

# Callback 7: Update 'Company' dropdown options based on 'Segmento' selection
@app.callback(
    Output('dropdown-company', 'options'),
    [Input('dropdown-setor', 'value'),
     Input('dropdown-subsetor', 'value'),
     Input('dropdown-segmento', 'value'),
     Input('store-data', 'data')]
)
def update_company_options(selected_setor, selected_subsetor, selected_segmento, stored_data):
    """
    Update the options of the 'Company' dropdown based on the selected 'Segmento'.
    """
    if selected_segmento is None or stored_data is None:
        raise dash.exceptions.PreventUpdate
    
    df = pd.DataFrame(stored_data)
    filtered_df = df[(df['SETOR'] == selected_setor) & (df['SUBSETOR'] == selected_subsetor) & (df['SEGMENTO'] == selected_segmento)]
    
    company_options = [{'label': company, 'value': company} for company in filtered_df['PREGAO'].sort_values().unique()]
    
    return company_options

# Callback 8: Toggle visibility and update 'Other Companies' options upon 'COMPANY' selection
@app.callback(
    [Output('multiselect-company', 'value'),
     Output('col-multiselect-company', 'style'),
     Output('multiselect-company', 'options')],
    [Input('dropdown-company', 'value'),
     Input('store-data', 'data')]
)
def manage_other_companies_on_company_change(selected_company, stored_data):
    """
    Manage the visibility and options of the 'Other Companies' multiselect dropdown upon 'COMPANY' selection.
    If a company is selected, the dropdown becomes visible and its options are populated, excluding the selected company.
    """
    if selected_company is None or stored_data is None:
        return [], {'display': 'none'}, []

    df = pd.DataFrame(stored_data)
    
    # Exclude the selected company
    other_companies = df[df['PREGAO'] != selected_company]['PREGAO'].sort_values().unique()
    other_company_options = [{'label': company, 'value': company} for company in other_companies]
    
    return [], {'display': 'block'}, other_company_options

# Callback 9: Display selected other companies
@app.callback(
    Output('display-other-companies', 'children'),
    Input('multiselect-company', 'value')
)
def display_selected_other_companies(selected_other_companies):
    """
    Display the selected companies from the 'Other Companies' multiselect dropdown.
    """
    if not selected_other_companies:
        return ""
    else:
        return f"Comparar com: {', '.join(selected_other_companies)}"

# Callback 10: Update stores and URL
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
    """
    Update stored data and URL based on the selected options from the dropdown menus.
    Depending on the selected options, navigate to the respective page.
    """
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
