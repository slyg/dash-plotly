import dash_apps.figures.build_status as build_status
import dash_apps.figures.duration as duration
import dash_apps.figures.failing_steps as failing_steps
import dash_apps.figures.heatmap as heatmap
import dash_apps.figures.lengthy_pipelines as lengthy_pipelines
import dash_apps.figures.most_failing as most_failing
import dash_apps.figures.nightly_vs_daily as nightly_vs_daily
import dash_apps.figures.timeline as timeline
import dash_apps.figures.timeline_short as timeline_short
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_apps.components.layout import layout
from dash_apps.components.navigation import getNavigation
from style.theme import BRAND


def set_layout(app):

    header = [getNavigation(app)]
    body = [
        html.Div(className='col col-12 col-xl-4 my-3',
                 children=[
                     html.Div(children=[
                         dcc.Loading(
                             color=BRAND, children=[dcc.Graph(id='build-status')])])
                 ]),
        html.Div(className='col col-12 col-xl-4 my-3',
                 children=[
                     html.Div(children=[
                         dcc.Loading(color=BRAND, children=[
                             dcc.Graph(id='build-status-14')])])
                 ]),
        html.Div(className='col col-12 col-xl-4 my-3',
                 children=[
                     html.Div(children=[
                         dcc.Loading(
                             color=BRAND, children=[dcc.Graph(id='nightly-vs-daily')])])
                 ]),
        html.Div(className='col col-12 my-3',
                 children=[
                     html.Div(children=[
                         dcc.Loading(
                             color=BRAND, children=[dcc.Graph(id='heatmap')])])
                 ]),
        html.Div(className='col col-12 my-3',
                 children=[
                     html.Div(children=[
                         dcc.Loading(
                             color=BRAND, children=[dcc.Graph(id='timeline-short')])])
                 ]),
        html.Div(className='col col-12 my-3',
                 children=[
                     html.Div(children=[
                         dcc.Loading(
                             color=BRAND, children=[dcc.Graph(id='most-failing')])])
                 ]),
        html.Div(className='col col-12 my-3',
                 children=[
                     html.Div(children=[
                         dcc.Loading(color=BRAND, children=[
                             dcc.Graph(id='failing-steps')])])
                 ]),
        html.Div(className='col col-12 my-3',
                 children=[
                     html.Div(children=[
                         dcc.Loading(color=BRAND, children=[
                             dcc.Graph(id='lengthy-pipelines')])])
                 ]),
        html.Div(className='col col-12 my-3',
                 children=[
                     html.Div(children=[
                         dcc.Loading(
                             color=BRAND, children=[dcc.Graph(id='duration')])])
                 ]),
        html.Div(className='col col-12 my-3',
                 children=[
                     html.Div(children=[
                         dcc.Loading(
                             color=BRAND, children=[dcc.Graph(id='timeline')])])
                 ]),
    ]

    app.layout = layout(app, header, body)

    @app.callback(Output('build-status', 'figure'), [Input('pipeline-type', 'value'), Input('project', 'value')])
    def build_status_update(pipeline_type, project):
        return build_status.get_fig(pipeline_type, project, 1)

    @app.callback(Output('build-status-14', 'figure'), [Input('pipeline-type', 'value'), Input('project', 'value')])
    def build_status_update_14(pipeline_type, project):
        return build_status.get_fig(pipeline_type, project)

    @app.callback(Output('heatmap', 'figure'), [Input('pipeline-type', 'value'), Input('project', 'value')])
    def heatmap_update(pipeline_type, project):
        return heatmap.get_fig(pipeline_type, project)

    @app.callback(Output('duration', 'figure'), [Input('pipeline-type', 'value'), Input('project', 'value')])
    def duration_update(pipeline_type, project):
        return duration.get_fig(pipeline_type, project)

    @app.callback(Output('failing-steps', 'figure'), [Input('pipeline-type', 'value'), Input('project', 'value')])
    def failing_steps_update(pipeline_type, project):
        return failing_steps.get_fig(pipeline_type, project)

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
