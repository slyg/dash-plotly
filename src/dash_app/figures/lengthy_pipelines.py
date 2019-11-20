import functools
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from dash_app.lib.events_28d import events
from dash_app.lib.nightly import select
from style.theme import TRANSPARENT, colors_map, colorscale, graph_title_font

days_in_past = 14
quantile = .75


@functools.lru_cache(maxsize=128)
def get_fig(selection):

    df = select(selection, events['df'])
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

    report = succeeding_pipelines_pivot[
        succeeding_pipelines_pivot['current_build_duration'] > succeeding_pipelines_pivot['current_build_duration'].quantile(
            quantile)
    ]

    layout = dict(
        title=go.layout.Title(text='Top {0}% lengthy succeeding pipelines ({1}) on {2} branch in the last {3} days<br>(generated on {4})'.format(
            round((1 - quantile) * 100), selection, branch, days_in_past, creation_time),
            font=graph_title_font
        ),
        autosize=True,
        paper_bgcolor=TRANSPARENT,
        plot_bgcolor=TRANSPARENT,
        bargap=0,
        yaxis=dict(
            automargin=True,
            ticksuffix=' —',
        ),
        xaxis=dict(
            title='Mean pipeline duration in minutes',
        ),
        height=600,
    )

    def get_bar(data_frame):
        return go.Bar(y=data_frame['job_name'],
                      x=data_frame['current_build_duration'].apply(
                          lambda x: x.total_seconds()/60),
                      width=1,
                      orientation='h',
                      marker={'color': data_frame['current_build_duration'],
                              'colorscale': colorscale['HueGradientInverted']}
                      )

    data = [get_bar(report)]

    figure = {
        'data': data,
        'layout': layout
    }

    return figure
