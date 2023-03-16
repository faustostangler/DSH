import dash

app = dash.Dash(__name__)
server = app.server

# Your app's layout and callbacks go here
if __name__ == "__main__":
    app.run_server(debug=True)
