import os.path
import time

import dash
import dash_core_components as dcc
import dash_html_components as html
import views.heatmap as heatmap
import views.last_day_master_build_status as last_day_master_build_status

external_stylesheets = [
    '//stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[


    html.Div(
        className='container-fluid',
        children=[
            html.Div(className='row my-3',
                     children=[
                         html.Div(className='col col-xl-12',
                                  children=[
                                      html.Div(className='navbar navbar-light bg-light',
                                               children=[
                                                   html.H1(className='navbar-brand',
                                                           children='RSE Dashboard'
                                                           )
                                               ]),
                                  ]),
                     ]),
            html.Div(
                className='row',
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
                ])
        ])
])

if __name__ == '__main__':
    app.run_server(debug=False, port=8050, host="0.0.0.0")
