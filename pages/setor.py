from dash import html, dcc, exceptions
from dash.dependencies import Input, Output

from app import app

# ----- LAYOUT -----
layout = html.Div([
    # Title of the page
    html.H1("Análise Fundamentalista"),
    
    # Subtitle that will be updated based on user selection
    html.H2(id='setor-title'),
    
    # Uncomment below lines to include additional content as needed.
    # Example: A graph that might be used to display some data.
    # dcc.Graph(id='graph-ativos'),
    
    # Additional contents here...
    # Include other HTML components and Dash components as per the design requirements.
])

# ----- CALLBACKS -----
# Callback to update the content based on the selected 'setor'
@app.callback(
    Output('setor-title', 'children'),  # Target component where updated data will be displayed
    Input('store-selected-setor', 'data')  # Source component which triggers the callback
)
def update_setor_content(stored_setor):
    # Check if there's any data stored, if not, prevent the update
    if stored_setor is None:
        raise exceptions.PreventUpdate
    
    # Retrieve 'setor' value from the stored data
    setor = stored_setor.get('setor', '')
    
    # Update the title based on the selected 'setor'
    # If 'setor' is available, display it as the subtitle; otherwise, display an empty string
    if setor:
        return f"{setor}"
    else:
        return ""
