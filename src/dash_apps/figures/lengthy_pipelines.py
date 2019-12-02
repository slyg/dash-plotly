import functools
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from dash_apps.lib.events_28d import events
from dash_apps.lib.filters import select
from style.theme import (TRANSPARENT, WHITE, colors_map, colorscale,
                         graph_title_font)

max_results = 50


@functools.lru_cache(maxsize=128)
def get_fig(pipeline_type, project, days_in_past=14):

    df = select(events['df'], pipeline_type, project)
    creation_time = events['creation_time']
    creation_time_iso = events['creation_time_iso']
    branch = events['branch']

    time_interval = timedelta(days=days_in_past)

    data_df = pd.DataFrame(
        df[df['current_build_scheduled_time'] > (
            creation_time_iso - time_interval).isoformat()]
        .sort_values(by='stage_timestamp')
        .drop_duplicates('build_tag', keep='last')
    )

    succeeding_pipelines = data_df[data_df['current_build_current_result'] == 'SUCCESS']

    succeeding_pipelines_pivot = pd.pivot_table(succeeding_pipelines,
                                                values=[
                                                    'current_build_duration'],
                                                index=['job_name'],
                                                aggfunc=lambda series: timedelta(milliseconds=round(series.mean())))\
        .sort_values(by='current_build_duration')\
        .reset_index()

    report = succeeding_pipelines_pivot.head(max_results)

    layout = dict(
        title=go.layout.Title(text='Top lengthy succeeding pipelines ({0}) on {1} branch in the last {2} days<br>(generated on {3})'.format(
            pipeline_type, branch, days_in_past, creation_time),
            font=graph_title_font
        ),
        autosize=True,
        paper_bgcolor=WHITE,
        plot_bgcolor=TRANSPARENT,
        bargap=0,
        yaxis=dict(
            automargin=True,
            ticksuffix=' —',
        ),
        xaxis=dict(
            title='Mean pipeline duration in minutes',
        ),
        height=(len(report) + 10) * 20,
    )

    def get_bar(data_frame):
        return go.Bar(y=data_frame['job_name'],
                      x=data_frame['current_build_duration'].apply(
                          lambda x: x.total_seconds()/60),
                      width=1,
                      orientation='h',
                      marker={'color': data_frame['current_build_duration'],
                              'colorscale': colorscale['HueGradient']}
                      )

    data = [get_bar(report)]

    figure = {
        'data': data,
        'layout': layout
    }

    return figure
