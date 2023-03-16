import dash
import dash_html_components as html

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Hello Dash')
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
