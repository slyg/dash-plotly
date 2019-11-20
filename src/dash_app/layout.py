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
from style.theme import BRAND


def set_layout(app):
    app.layout = html.Div(children=[
        html.Div(
            className='container-fluid',
            children=[
                html.Div(
                    className='row my-3',
                    children=[
                        html.Div(className='col col-12',
                                 children=[
                                     html.Nav(className='navbar fixed-top navbar-light py-0',
                                              style={
                                                  'background-color': 'rgba(245, 245, 245, 0.8)',
                                                  'border-bottom': '2px solid {0}'.format(BRAND)
                                              },
                                              children=[
                                                  html.H1(className='navbar-brand my-0',
                                                          children=[
                                                              html.Img(className='d-inline-block align-middle pb-1',
                                                                       src=app.get_asset_url(
                                                                           'RSE-community-logo.svg'),
                                                                       width='40',
                                                                       height='40'
                                                                       ),
                                                              html.Span(className='d-inline-block pl-2 mt-2',
                                                                        children='RSE Dashboard'
                                                                        ),
                                                          ]),
                                                  html.Div(className='form-inline my-2 my-lg-0',
                                                           children=[
                                                               html.Span(className='d-inline-block pr-2 py-2 text-dark small',
                                                                         children='Nightly / Non-nightly'
                                                                         ),
                                                               dcc.Dropdown(
                                                                   id="nightly",
                                                                   className="small",
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
                    className='row mt-5',
                    children=[
                        html.Div(className='col col-12 col-xl-4 my-3',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='build-status'))])
                                 ]),
                        html.Div(className='col col-12 col-xl-4 my-3',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='build-status-72'))])
                                 ]),
                        html.Div(className='col col-12 col-xl-4 my-3',
                                 children=[
                                     html.Div(className='p-3 bg-light',
                                              children=[dcc.Loading(dcc.Graph(id='nightly-vs-daily', figure=nightly_vs_daily.get_fig()))])
                                 ]),
                        html.Div(className='col col-12 my-3',
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

    @app.callback(Output('build-status', 'figure'), [Input('nightly', 'value')])
    def build_status_update(selection):
        return build_status.get_fig(selection)

    @app.callback(Output('build-status-72', 'figure'), [Input('nightly', 'value')])
    def build_status_update(selection):
        return build_status.get_fig(selection, 72)

    @app.callback(Output('heatmap', 'figure'), [Input('nightly', 'value')])
    def heatmap_update(selection):
        return heatmap.get_fig(selection)

    @app.callback(Output('duration', 'figure'), [Input('nightly', 'value')])
    def duration_update(selection):
        return duration.get_fig(selection)

    @app.callback(Output('failing-steps', 'figure'), [Input('nightly', 'value')])
    def failing_steps_update(selection):
        return failing_steps.get_fig(selection)

    @app.callback(Output('failing-steps-pie', 'figure'), [Input('nightly', 'value')])
    def failing_steps_pie_update(selection):
        return failing_steps_pie.get_fig(selection)

    @app.callback(Output('most-failing', 'figure'), [Input('nightly', 'value')])
    def most_failing_update(selection):
        return most_failing.get_fig(selection)

    @app.callback(Output('timeline-short', 'figure'), [Input('nightly', 'value')])
    def timeline_short_update(selection):
        return timeline_short.get_fig(selection)

    @app.callback(Output('lengthy-pipelines', 'figure'), [Input('nightly', 'value')])
    def lengthy_pipelines_update(selection):
        return lengthy_pipelines.get_fig(selection)

    @app.callback(Output('timeline', 'figure'), [Input('nightly', 'value')])
    def timeline_update(selection):
        return timeline.get_fig(selection)
