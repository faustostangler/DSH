from dash import html, dcc
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    html.H2(id='segmento-title'),
    dcc.Graph(id='graph-ativos'),
    # Your contents here...
])

# Callbacks for this page...

def update_segmento_content(stored_setor, stored_subsetor, stored_segmento):
    if stored_setor is None or stored_subsetor is None or stored_segmento is None:
        raise dash.exceptions.PreventUpdate
    
    setor = stored_setor.get('setor', '')
    subsetor = stored_subsetor.get('subsetor', '')
    segmento = stored_subsetor.get('segmento', '')
    if segmento:
        return f"{setor} - {subsetor} - {segmento}"
    else:
        return ""
