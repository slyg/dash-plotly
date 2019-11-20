import functools
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from dash_app.lib.events_28d import events
from dash_app.lib.filters import select_project
from style.theme import TRANSPARENT, WHITE, colors_map, graph_title_font

days_in_the_past = 14


@functools.lru_cache(maxsize=128)
def get_fig(project):

    df = select_project(events['df'], project)
    creation_time = events['creation_time']
    creation_time_iso = events['creation_time_iso']
    branch = events['branch']

    one_day = timedelta(days=1)
    max_past_date = (creation_time_iso -
                     (days_in_the_past * one_day)).isoformat()

    last_builds = df[df['stage_timestamp'] > max_past_date]
    last_builds = last_builds.sort_values(
        by='stage_timestamp').drop_duplicates('build_tag', keep='last')

    failures_df = last_builds[
        (last_builds['current_build_current_result'] == 'FAILURE')
        | (last_builds['current_build_current_result'] == 'ABORTED')]

    failures_nightly_df = failures_df[last_builds['job_name'].str.contains(
        "HMCTS_Nightly") == False]

    failures_nightly = len(failures_nightly_df.index)
    failures_daily = len(failures_df.index) - failures_nightly

    values = [failures_nightly, failures_daily]

    labels = ['Nightly',
              'Non-nightly']

    colors = ['rgb(97,88,218)', 'rgb(98,172,214)']

    layout = dict(
        title=go.layout.Title(text='Nightly vs non-nightly failures for {0} CI pipelines <br>in the last {1} days<br>(generated on {2})'.format(branch, days_in_the_past, creation_time),
                              font=graph_title_font
                              ),
        paper_bgcolor=WHITE,
        plot_bgcolor=TRANSPARENT,
    )

    pie = go.Pie(labels=labels,
                 values=values,
                 marker=dict(colors=colors,
                             line=dict(color=WHITE, width=1))
                 )

    figure = {'data': [pie],
              'layout': layout
              }

    return figure
