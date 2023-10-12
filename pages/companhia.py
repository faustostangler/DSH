from dash import html, dcc
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    html.H3(id='segmento-title'),
    html.H2(id='company-title'),
    # Your content here...
    dcc.Graph(id='graph-ativos'),
])

@app.callback(
    Output('company-title', 'children'),
    Input('store-selected-company', 'data')
)
def update_company_title(stored_company):
    if stored_company is None:
        return "Selecione uma Empresa"
    return f"{stored_company['company']}"


