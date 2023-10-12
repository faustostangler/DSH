from dash import html, dcc
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    html.H2("Setor Page"),
    html.H3(id='setor-title'),
    dcc.Graph(id='graph-ativos'),
    # Your contents here...
])

# Callbacks for this page...
# update the content based on the selected 'setor'
@app.callback(
    Output('setor-title', 'children'),
    Input('store-selected-setor', 'data')
)
def update_setor_content(stored_setor):
    if stored_setor is None:
        raise dash.exceptions.PreventUpdate
    
    setor = stored_setor.get('setor', '')
    if setor:
        return f"Content for Setor: {setor}"
    else:
        return ""