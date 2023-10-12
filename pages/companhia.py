from dash import html, dcc, exceptions
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    html.H1("Análise Fundamentalista"),
    html.H2(id='company-segmento-title'), 
    html.H2(id='company-title'),
    # Your content here...
    dcc.Graph(id='graph-ativos'),
])


@app.callback(
    [Output('company-segmento-title', 'children'),
     Output('company-title', 'children')],
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
    if companhia:
        segmento_title = f"{setor} - {subsetor} - {segmento}"
        company_title = companhia
    else:
        segmento_title = ''
        company_title = ''

    return segmento_title, company_title
