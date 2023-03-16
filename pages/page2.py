import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/dry', name='Step 2')

df = px.data.tips()

layout = html.Div(
    [
        dcc.RadioItems([x for x in df.day.unique()], id='day-choice'),
        dcc.Graph(id='bar-fig',
                  figure=px.bar(df, x='smoker', y='total_bill'))
    ]
)
