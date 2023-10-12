from dash import html, dcc
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    html.H2("Subsetor Page"),
    html.H3(id='subsetor-title'),
    dcc.Graph(id='graph-ativos'),
    # Your contents here...
])

# Callbacks for this page...
# update the content based on the selected 'setor' and 'subsetor'
@app.callback(
    Output('subsetor-title', 'children'),
    [Input('store-selected-setor', 'data'),
     Input('store-selected-subsetor', 'data')]
)
def update_subsetor_content(stored_setor, stored_subsetor):
    if stored_setor is None or stored_subsetor is None:
        raise dash.exceptions.PreventUpdate
    
    setor = stored_setor.get('setor', '')
    subsetor = stored_subsetor.get('subsetor', '')
    return f"Content for Setor: {setor}, Subsetor: {subsetor}"
    if subsetor:
        return f"Content: {setor} - {subsetor}"
    else:
        return ""

