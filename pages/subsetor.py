from dash import html, dcc, exceptions
from dash.dependencies import Input, Output

from app import app

# ----- LAYOUT -----
layout = html.Div([
    # Main title of the page
    html.H1("Análise Fundamentalista"),
    
    # Subtitle that will be updated based on user selection
    html.H2(id='subsetor-title'),
    
    # Additional contents might go here, like graphs, tables, etc.
    # Uncomment and adjust the following line as per your requirements.
    # dcc.Graph(id='graph-ativos'),
    
    # More contents here...
])

# ----- CALLBACKS -----
# Callback to update the content based on the selected 'setor' and 'subsetor'
@app.callback(
    Output('subsetor-title', 'children'),  # Target component to display the updated data
    [Input('store-selected-setor', 'data'),  # Source component which triggers the callback
     Input('store-selected-subsetor', 'data')]  # Another source component for the callback
)
def update_subsetor_content(stored_setor, stored_subsetor):
    """
    Update the subtitle based on selected 'setor' and 'subsetor'.

    Parameters:
    - stored_setor (dict): Stored data for selected 'setor'.
    - stored_subsetor (dict): Stored data for selected 'subsetor'.

    Returns:
    - str: Updated subtitle string containing 'setor' and 'subsetor'.
    """
    # Check if there's any data stored, if not, prevent the update
    if stored_setor is None or stored_subsetor is None:
        raise exceptions.PreventUpdate
    
    # Retrieve 'setor' and 'subsetor' values from the stored data
    setor = stored_setor.get('setor', '')
    subsetor = stored_subsetor.get('subsetor', '')
    
    # Update the title based on the selected 'setor' and 'subsetor'
    # If 'subsetor' is available, display it along with 'setor' as the subtitle; otherwise, display an empty string
    if subsetor:
        return f"{setor} - {subsetor}"
    else:
        return ""
