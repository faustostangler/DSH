from dash import html, dcc, exceptions
from dash.dependencies import Input, Output

from app import app

# ----- LAYOUT -----
layout = html.Div([
    # Main title of the page
    html.H1("Análise Fundamentalista"),
    
    # Subtitle that will be updated based on user selection
    html.H2(id='segmento-title'),
    
    # Additional contents might go here, like graphs, tables, etc.
    # Uncomment and adjust the following line as per your requirements.
    # dcc.Graph(id='graph-ativos'),
    
    # More contents here...
])

# ----- CALLBACKS -----
@app.callback(
    Output('segmento-title', 'children'),  # Target component to display the updated data
    [Input('store-selected-setor', 'data'),  # Source component which triggers the callback
     Input('store-selected-subsetor', 'data'),  # Another source component for the callback
     Input('store-selected-segmento', 'data')]  # Another source component for the callback
)
def update_segmento_content(stored_setor, stored_subsetor, stored_segmento):
    """
    Update the subtitle based on selected 'setor', 'subsetor', and 'segmento'.

    Parameters:
    - stored_setor (dict): Stored data for selected 'setor'.
    - stored_subsetor (dict): Stored data for selected 'subsetor'.
    - stored_segmento (dict): Stored data for selected 'segmento'.

    Returns:
    - str: Updated subtitle string containing 'setor', 'subsetor', and 'segmento'.
    """
    # Check if there's any data stored, if not, prevent the update
    if stored_setor is None or stored_subsetor is None or stored_segmento is None:
        raise exceptions.PreventUpdate
    
    # Retrieve 'setor', 'subsetor', and 'segmento' values from the stored data
    setor = stored_setor.get('setor', '')
    subsetor = stored_subsetor.get('subsetor', '')
    segmento = stored_segmento.get('segmento', '')
    
    # Update the title based on the selected 'setor', 'subsetor', and 'segmento'
    # If 'segmento' is available, display it along with 'setor' and 'subsetor' as the subtitle; otherwise, display an empty string
    if segmento:
        return f"{setor} - {subsetor} - {segmento}"
    else:
        return ""
