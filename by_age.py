# Import packages
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
# import dash_bootstrap_components as dbc

# Incorporate data
df = pd.read_csv('conneticut_wide_form.csv')

# Initialize the app - incorporate a Dash Bootstrap theme
# external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__) #, external_stylesheets=external_stylesheets)

age_fig = px.histogram(df, x='age')

app.layout = html.Div(children=[
    html.H1("Histogram of Ages"),
    dcc.Input(
        id='bin-width',
        type='number',
        value=5,
        min=1,
        step=1,
        placeholder="Enter bin width",
        style={'margin-bottom': '10px'}
    ),
    dcc.Graph(id='histogram')
])

@callback(
    Output('histogram', 'figure'),
    Input('bin-width', 'value'))
def update_histogram_bins(bin_width):
    if bin_width is None or bin_width <= 0:
        bin_width = 5
    fig = px.histogram(
        df,
        x='age',
        title='By Age',
        # labels={'Age': 'Agelabe', 'count': 'Count of People labe'}
    )
    fig.update_traces(xbins=dict(size=bin_width))
    fig.update_layout(xaxis_title='Age', yaxis_title='Count', bargap=0.1)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
