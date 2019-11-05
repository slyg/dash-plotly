import os.path
import time

import dash
import dash_core_components as dcc
import dash_html_components as html
import views.build_status as build_status
import views.heatmap as heatmap
import views.most_failing as most_failing
import views.timeline as timeline
import views.timeline_short as timeline_short
from dash.dependencies import Input, Output

external_stylesheets = [
    '//stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "RSE Dashboard"
app.layout = html.Div(children=[
    dcc.Interval(
        id='short-term-interval',
        interval=5*60*1000,  # 5 min
        n_intervals=0
    ),
    html.Div(
        className='container-fluid',
        children=[
            html.Div(
                className='row my-4',
                children=[
                    html.Div(className='col col-xl-12',
                             children=[
                                 html.Nav(className='navbar navbar-light bg-light',
                                          children=[
                                              html.H1(className='navbar-brand',
                                                      children=[
                                                          html.Img(className='d-inline-block align-top',
                                                                   src=app.get_asset_url(
                                                                       'RSE-community-logo.svg'),
                                                                   width='30',
                                                                   height='30'
                                                                   ),
                                                          html.Span(className='pl-2',
                                                                    children='RSE Dashboard'
                                                                    )
                                                      ])
                                          ]),
                             ]),
                ]),
            html.Div(
                className='row mb-4',
                children=[
                    html.Div(className='col col-xl-4',
                             children=[
                                 html.Div(className='p-3 bg-light',
                                          children=[dcc.Graph(id='build-status')])
                             ]),
                    html.Div(className='col col-xl-8',
                             children=[
                                 html.Div(className='p-3 bg-light',
                                          children=[dcc.Graph(id='heatmap')])
                             ])
                ]),
            html.Div(
                className='row mb-4',
                children=[
                    html.Div(className='col col-xl-12',
                             children=[
                                 html.Div(className='p-3 bg-light',
                                          children=[dcc.Graph(id='timeline-short')])
                             ])
                ]),
            html.Div(
                className='row mb-4',
                children=[
                    html.Div(className='col col-xl-12',
                             children=[
                                 html.Div(className='p-3 bg-light',
                                          children=[dcc.Graph(id='most-failing')])
                             ])
                ]),
            html.Div(
                className='row mb-4',
                children=[
                    html.Div(className='col col-xl-12',
                             children=[
                                 html.Div(className='p-3 bg-light',
                                          children=[dcc.Graph(
                                              figure=timeline.get_fig())]
                                          )
                             ])
                ]),
        ])
])

# Compute short-term graphs updates

@app.callback(Output('build-status', 'figure'),
              [Input('short-term-interval', 'n_intervals')])
def build_status_update(n):
    return build_status.get_fig()

@app.callback(Output('heatmap', 'figure'),
              [Input('short-term-interval', 'n_intervals')])
def heatmap_update(n):
    return heatmap.get_fig()

@app.callback(Output('most-failing', 'figure'),
              [Input('short-term-interval', 'n_intervals')])
def most_failing_update(n):
    return most_failing.get_fig()

@app.callback(Output('timeline-short', 'figure'),
              [Input('short-term-interval', 'n_intervals')])
def timeline_short_update(n):
    return timeline_short.get_fig()


if __name__ == '__main__':
    app.run_server(debug=False, port=8050, host="0.0.0.0")
