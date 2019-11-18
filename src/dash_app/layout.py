import dash_app.figures.build_status as build_status
import dash_app.figures.duration as duration
import dash_app.figures.failing_steps as failing_steps
import dash_app.figures.failing_steps_pie as failing_steps_pie
import dash_app.figures.heatmap as heatmap
import dash_app.figures.lengthy_pipelines as lengthy_pipelines
import dash_app.figures.most_failing as most_failing
import dash_app.figures.nightly_vs_daily as nightly_vs_daily
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
                    className='row my-3',
                    children=[
                        html.Div(className='col col-12',
                                 children=[
                                     html.Nav(className='navbar navbar-light bg-light',
                                              children=[
                                                  html.H1(className='navbar-brand',
                                                          children=[
                                                              html.Img(className='d-inline-block align-top',
                                                                       src=app.get_asset_url(
                                                                           'RSE-community-logo.svg'),
                                                                       width='45',
                                                                       height='45'
                                                                       ),
                                                              html.Span(className='d-inline-block pl-2 py-2',
                                                                        children='RSE Dashboard'
                                                                        ),
                                                          ]),
                                                  html.Div(className='form-inline my-2 my-lg-0',
                                                           children=[
                                                               html.Span(className='d-inline-block pr-2 py-2',
                                                                         children='Nightly/Non-nightly'
                                                                         ),
                                                               dcc.Dropdown(
                                                                   id="nightly",
                                                                   clearable=False,
                                                                   style={
                                                                       'width': 200},
                                                                   options=[
                                                                       {'label': 'Nightly',
                                                                        'value': 'nightly'},
                                                                       {'label': 'Non-nightly',
                                                                        'value': 'non-nightly'},
                                                                       {'label': 'All',
                                                                        'value': 'all'},
                                                                   ],
                                                                   value='all'),
                                                           ])
                                              ]),
                                 ]),
                    ]),
                html.Div(
                    className='row',
                    children=[
                        html.Div(className='col col-12 col-xl-4 my-3',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='build-status'))])
                                 ]),
                        html.Div(className='col col-12 col-xl-8 my-3',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='heatmap'))])
                                 ]),
                        html.Div(className='col col-12 my-3',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='timeline-short'))])
                                 ]),
                        html.Div(className='col col-12 my-3',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='nightly-vs-daily'))])
                                 ]),
                        html.Div(className='col col-12 my-3',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='most-failing'))])
                                 ]),
                        html.Div(className='col col-12 my-3',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='failing-steps-pie'))])
                                 ]),
                        html.Div(className='col col-12 my-3',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='failing-steps'))])
                                 ]),
                        html.Div(className='col col-12 my-3',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='lengthy-pipelines'))])
                                 ]),
                        html.Div(className='col col-12 my-3',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='duration'))])
                                 ]),
                        html.Div(className='col col-12 my-3',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='timeline'))])
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

    @app.callback(Output('duration', 'figure'), [Input('nightly', 'value'), Input('short-term-interval', 'n_intervals')])
    def duration_update(selection, n):
        return duration.get_fig(selection)

    @app.callback(Output('failing-steps', 'figure'), interval_inputs)
    def failing_steps_update(n):
        return failing_steps.get_fig()

    @app.callback(Output('failing-steps-pie', 'figure'), interval_inputs)
    def failing_steps_pie_update(n):
        return failing_steps_pie.get_fig()

    @app.callback(Output('most-failing', 'figure'), interval_inputs)
    def most_failing_update(n):
        return most_failing.get_fig()

    @app.callback(Output('timeline-short', 'figure'), interval_inputs)
    def timeline_short_update(n):
        return timeline_short.get_fig()

    @app.callback(Output('lengthy-pipelines', 'figure'), interval_inputs)
    def lengthy_pipelines_update(n):
        return lengthy_pipelines.get_fig()

    @app.callback(Output('nightly-vs-daily', 'figure'), interval_inputs)
    def nigthly_vs_daily_update(n):
        return nightly_vs_daily.get_fig()

    @app.callback(Output('timeline', 'figure'), [Input('nightly', 'value')])
    def timeline_update(selection):
        return timeline.get_fig(selection)
