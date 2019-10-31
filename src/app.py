import os.path
import time

import dash
import dash_core_components as dcc
import dash_html_components as html
import views.heatmap as heatmap
import views.last_day_master_build_status as last_day_master_build_status
import views.timeline as timeline

external_stylesheets = [
    '//stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[


    html.Div(
        className='container-fluid',
        children=[
            html.Div(className='row my-4',
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
                                          children=[
                                              dcc.Graph(
                                                  figure=last_day_master_build_status.figure)
                                          ])
                             ]),
                    html.Div(className='col col-xl-8',
                             children=[
                                 html.Div(className='p-3 bg-light',
                                          children=[
                                              dcc.Graph(figure=heatmap.figure)
                                          ])
                             ])
                ]),
            html.Div(
                className='row mb-4',
                children=[
                    html.Div(className='col col-xl-12',
                             children=[
                                 html.Div(className='p-3 bg-light',
                                          children=[
                                              dcc.Graph(
                                                  figure=timeline.figure)
                                          ])
                             ])
                ])
        ])
])

if __name__ == '__main__':
    app.run_server(debug=False, port=8050, host="0.0.0.0")
