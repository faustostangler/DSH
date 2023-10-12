import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

from app import app

import assets.helper as b3
# import assets.variables as var
# import assets.system_variables as varsys
# import assets.system_functions as runsys

# dash.register_page(__name__, path='/setup', name='Setup and Config')

options = dcc.RadioItems(id='options', options={
    'b3_companies': 'Atualizar Companhias da B3',
    'world_markets': 'Atualizar Mercados Mundiais',
    'yahoo_cotahist': 'Atualizar Cotações Brasileiras pelo Yahoo! Finance',
    'get_nsd_links': 'Atualizar os registros NSD da B3 Bovespa', 
    'get_dre': 'Atualizar os demonstrativos financeiros DRE da B3 Bovespa', 
    'other': 'Outras opções',
    }, 
    labelStyle={'display': 'block'}, 
    inputClassName='form-check-input',
    labelClassName='form-check-label form-check-inline'
    ),


layout = html.Div([
            html.H2(['Atualização do Banco de Dados']), 
            html.H3(['Escolha qual opção você deseja atualizar']), 
            html.Div(
                options, 
            ), 
            html.Div(id='result', children=[]), 
])



@callback(
    Output('result', 'children'),
    Input('options', 'value'), 
    prevent_initial_call=True, 
)
def options(value):
    if value == 'b3_companies':
        value = b3.update_b3_companies(value)
    if value == 'world_markets':
        value = b3.update_world_markets(value)
    if value == 'yahoo_cotahist':
        value = b3.yahoo_cotahist(value)
    if value == 'get_nsd_links':
        value = b3.get_nsd_links(value)
    if value == 'get_dre':
        value = b3.get_dre(value)

        
    return value

    

def show_b3(value):
    table = html.Div([
        value, 
    # dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, )
    ])

    return table

