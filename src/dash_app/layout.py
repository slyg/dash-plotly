import dash_app.figures.build_status as build_status
import dash_app.figures.duration as duration
import dash_app.figures.heatmap as heatmap
import dash_app.figures.most_failing as most_failing
import dash_app.figures.timeline as timeline
import dash_app.figures.timeline_short as timeline_short
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


def set_layout(app):
    app.layout = html.Div(children=[
        dcc.Interval(
            id='short-term-interval',
            interval=60*60*1000,  # 1 hour
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
                                              children=[dcc.Loading(dcc.Graph(id='build-status'))])
                                 ]),
                        html.Div(className='col col-xl-8',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='heatmap'))])
                                 ])
                    ]),
                html.Div(
                    className='row mb-4',
                    children=[
                        html.Div(className='col col-xl-12',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='timeline-short'))])
                                 ])
                    ]),
                html.Div(
                    className='row mb-4',
                    children=[
                        html.Div(className='col col-xl-12',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='most-failing'))])
                                 ])
                    ]),
                html.Div(
                    className='row mb-4',
                    children=[
                        html.Div(className='col col-xl-12',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='duration'))])
                                 ])
                    ]),
                html.Div(
                    className='row mb-4',
                    children=[
                        html.Div(className='col col-xl-12',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(
                                                  figure=timeline.get_fig()))]
                                              )
                                 ])
                    ]),
            ])
    ])

    # Compute short-term graphs updates

    interval_inputs = [Input('short-term-interval', 'n_intervals')]

    @app.callback(Output('build-status', 'figure'), interval_inputs)
    def build_status_update(n):
        return build_status.get_fig()

    @app.callback(Output('heatmap', 'figure'), interval_inputs)
    def heatmap_update(n):
        return heatmap.get_fig()

    @app.callback(Output('duration', 'figure'), interval_inputs)
    def duration_update(n):
        return duration.get_fig()

    @app.callback(Output('most-failing', 'figure'), interval_inputs)
    def most_failing_update(n):
        return most_failing.get_fig()

    @app.callback(Output('timeline-short', 'figure'), interval_inputs)
    def timeline_short_update(n):
        return timeline_short.get_fig()