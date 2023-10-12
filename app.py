# Import necessary libraries
import dash  # Import the Dash framework
import dash_bootstrap_components as dbc  # Import Bootstrap components

# Note: The below imports are placeholders and will depend on your project's structure.
# import importlib  # Import the Python standard module for importing modules programmatically 
# import os  # Import the Python standard module to interact with the operating system

# Initialize the Dash app
# `suppress_callback_exceptions=True` allows defining callbacks that are not in the initial layout of the app
# `external_stylesheets` parameter is utilized to apply external styles to the app, here using Bootstrap's theme.
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# `server` attribute is an instance of Flask, which can be used to run the app
# It can also be utilized to serve the app in production using a WSGI server like gunicorn
server = app.server
