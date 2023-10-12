from dash import html, dcc, exceptions
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    html.H1("Análise Fundamentalista"),
    html.H2(id='segmento-title'),
    # Your contents here...
    dcc.Graph(id='graph-ativos'),
])

# Callbacks for this page...

@app.callback(
    Output('segmento-title', 'children'),
    [Input('store-selected-setor', 'data'),
     Input('store-selected-subsetor', 'data'),
     Input('store-selected-segmento', 'data')]
)
def update_segmento_content(stored_setor, stored_subsetor, stored_segmento):
    if stored_setor is None or stored_subsetor is None or stored_segmento is None:
        raise exceptions.PreventUpdate
    
    setor = stored_setor.get('setor', '')
    subsetor = stored_subsetor.get('subsetor', '')
    segmento = stored_segmento.get('segmento', '')  # Fixed this line
    if segmento:
        return f"{setor} - {subsetor} - {segmento}"
    else:
        return ""
