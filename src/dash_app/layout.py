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
from style.theme import BRAND, LIGHT_GREY, WHITE_ALPHA_8


def set_layout(app):
    app.layout = html.Div(children=[
        html.Div(
            className='container-fluid',
            style={
                'background-color': LIGHT_GREY,
            },
            children=[
                html.Div(
                    className='row my-3',
                    children=[
                        html.Div(className='col col-12',
                                 children=[
                                     html.Nav(className='navbar fixed-top navbar-light py-0',
                                              style={
                                                  'background-color': WHITE_ALPHA_8,
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
                                                               html.Form(className="pl-5",
                                                                        children=[
                                                                            html.Span(className='d-inline-block pr-2 py-2 text-dark small',
                                                                                        children='Project'
                                                                                        ),
                                                                            html.Div(className="d-inline-block align-middle",
                                                                                        children=[
                                                                                            dcc.Dropdown(
                                                                                                id="project",
                                                                                                className="small",
                                                                                                clearable=False,
                                                                                                style={
                                                                                                    'width': 200},
                                                                                                options=[
                                                                                                    {'label': 'All',
                                                                                                    'value': 'all'},

                                                                                                    {'label': 'Bulk Scanning',
                                                                                                    'value': '_BSP'},

                                                                                                    {'label': 'CCD',
                                                                                                    'value': '_CDM'},

                                                                                                    {'label': 'CMC',
                                                                                                    'value': '_CMC'},

                                                                                                    {'label': 'CTSC',
                                                                                                    'value': '_CTSC'},

                                                                                                    {'label': 'DIV',
                                                                                                    'value': '_DIV'},

                                                                                                    {'label': 'FeePay',
                                                                                                    'value': '_FeePay'},

                                                                                                    {'label': 'FinRem',
                                                                                                    'value': '_FinRem'},

                                                                                                    {'label': 'Platform',
                                                                                                    'value': '_Platform'},

                                                                                                    {'label': 'Probate',
                                                                                                    'value': '_Probate'},

                                                                                                    {'label': 'RPA',
                                                                                                    'value': '_RPA'},

                                                                                                    {'label': 'SCSS',
                                                                                                    'value': '_SSCS'},
                                                                                                ],
                                                                                                value='all'),
                                                                                        ])
                                                                        ]),
                                                               html.Form(className="pl-5",
                                                                        children=[
                                                                            html.Span(className='d-inline-block pr-2 py-2 text-dark small',
                                                                                        children='Nightly / Non-nightly'
                                                                                        ),
                                                                            html.Div(className="d-inline-block align-middle",
                                                                                        children=[
                                                                                            dcc.Dropdown(id="pipeline-type",
                                                                                                        clearable=False,
                                                                                                        className="small",
                                                                                                        style={
                                                                                                            'width': 200},
                                                                                                        options=[
                                                                                                            {'label': 'All',
                                                                                                            'value': 'all'},
                                                                                                            {'label': 'Nightly',
                                                                                                            'value': 'nightly'},
                                                                                                            {'label': 'Non-nightly',
                                                                                                            'value': 'non-nightly'},
                                                                                                        ],
                                                                                                        value='all'),
                                                                                        ])
                                                                        ])


                                                           ]),
                                              ]),
                                 ]),
                    ]),
                html.Div(
                    className='row mt-5',
                    children=[
                        html.Div(className='col col-12 col-xl-4 my-3',
                                 children=[
                                     html.Div(children=[dcc.Loading(
                                         color=BRAND, children=[dcc.Graph(id='build-status')])])
                                 ]),
                        html.Div(className='col col-12 col-xl-4 my-3',
                                 children=[
                                     html.Div(children=[dcc.Loading(color=BRAND, children=[
                                              dcc.Graph(id='build-status-72')])])
                                 ]),
                        html.Div(className='col col-12 col-xl-4 my-3',
                                 children=[
                                     html.Div(children=[dcc.Loading(
                                         color=BRAND, children=[dcc.Graph(id='nightly-vs-daily')])])
                                 ]),
                        html.Div(className='col col-12 my-3',
                                 children=[
                                     html.Div(children=[dcc.Loading(
                                         color=BRAND, children=[dcc.Graph(id='heatmap')])])
                                 ]),
                        html.Div(className='col col-12 my-3',
                                 children=[
                                     html.Div(children=[dcc.Loading(
                                         color=BRAND, children=[dcc.Graph(id='timeline-short')])])
                                 ]),
                        html.Div(className='col col-12 my-3',
                                 children=[
                                     html.Div(children=[dcc.Loading(
                                         color=BRAND, children=[dcc.Graph(id='most-failing')])])
                                 ]),
                        html.Div(className='col col-12 my-3',
                                 children=[
                                     html.Div(children=[dcc.Loading(color=BRAND, children=[
                                              dcc.Graph(id='failing-steps-pie')])])
                                 ]),
                        html.Div(className='col col-12 my-3',
                                 children=[
                                     html.Div(children=[dcc.Loading(
                                         color=BRAND, children=[dcc.Graph(id='failing-steps')])])
                                 ]),
                        html.Div(className='col col-12 my-3',
                                 children=[
                                     html.Div(children=[dcc.Loading(color=BRAND, children=[
                                              dcc.Graph(id='lengthy-pipelines')])])
                                 ]),
                        html.Div(className='col col-12 my-3',
                                 children=[
                                     html.Div(children=[dcc.Loading(
                                         color=BRAND, children=[dcc.Graph(id='duration')])])
                                 ]),
                        html.Div(className='col col-12 my-3',
                                 children=[
                                     html.Div(children=[dcc.Loading(
                                         color=BRAND, children=[dcc.Graph(id='timeline')])])
                                 ])
                    ]),
            ])
    ])

    @app.callback(Output('build-status', 'figure'), [Input('pipeline-type', 'value'), Input('project', 'value')])
    def build_status_update(pipeline_type, project):
        return build_status.get_fig(pipeline_type, 24, project)

    @app.callback(Output('build-status-72', 'figure'), [Input('pipeline-type', 'value'), Input('project', 'value')])
    def build_status_update_72(pipeline_type, project):
        return build_status.get_fig(pipeline_type, 72, project)

    @app.callback(Output('heatmap', 'figure'), [Input('pipeline-type', 'value'), Input('project', 'value')])
    def heatmap_update(pipeline_type, project):
        return heatmap.get_fig(pipeline_type, project)

    @app.callback(Output('duration', 'figure'), [Input('pipeline-type', 'value'), Input('project', 'value')])
    def duration_update(pipeline_type, project):
        return duration.get_fig(pipeline_type, project)

    @app.callback(Output('failing-steps', 'figure'), [Input('pipeline-type', 'value'), Input('project', 'value')])
    def failing_steps_update(pipeline_type, project):
        return failing_steps.get_fig(pipeline_type, project)

    @app.callback(Output('failing-steps-pie', 'figure'), [Input('pipeline-type', 'value'), Input('project', 'value')])
    def failing_steps_pie_update(pipeline_type, project):
        return failing_steps_pie.get_fig(pipeline_type, project)

    @app.callback(Output('most-failing', 'figure'), [Input('pipeline-type', 'value'), Input('project', 'value')])
    def most_failing_update(pipeline_type, project):
        return most_failing.get_fig(pipeline_type, project)

    @app.callback(Output('timeline-short', 'figure'), [Input('pipeline-type', 'value'), Input('project', 'value')])
    def timeline_short_update(pipeline_type, project):
        return timeline_short.get_fig(pipeline_type, project)

    @app.callback(Output('lengthy-pipelines', 'figure'), [Input('pipeline-type', 'value'), Input('project', 'value')])
    def lengthy_pipelines_update(pipeline_type, project):
        return lengthy_pipelines.get_fig(pipeline_type, project)

    @app.callback(Output('timeline', 'figure'), [Input('pipeline-type', 'value'), Input('project', 'value')])
    def timeline_update(pipeline_type, project):
        return timeline.get_fig(pipeline_type, project)

    @app.callback(Output('nightly-vs-daily', 'figure'), [Input('project', 'value')])
    def nightly_vs_daily_update(project):
        return nightly_vs_daily.get_fig(project)
