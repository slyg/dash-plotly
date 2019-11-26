import functools
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from dash_app.lib.events_28d import events
from dash_app.lib.filters import select
from style.theme import (TRANSPARENT, WHITE, colors_map, graph_title_font,
                         pie_line_style)


@functools.lru_cache(maxsize=128)
def get_fig(pipeline_type, project, number_of_days=14):

    df = select(events['df'], pipeline_type, project)
    creation_time = events['creation_time']
    creation_time_iso = events['creation_time_iso']
    branch = events['branch']

    one_day = timedelta(hours=24)
    max_past_date = (creation_time_iso -
                     (number_of_days * one_day)).isoformat()

    last_builds = df[df['stage_timestamp'] > max_past_date]
    last_builds = last_builds.sort_values(
        by='stage_timestamp').drop_duplicates('build_tag', keep='last')

    total_rows = len(last_builds)
    successes = len(
        last_builds.loc[last_builds['current_build_current_result'] == 'SUCCESS'])
    failures = len(
        last_builds.loc[last_builds['current_build_current_result'] == 'FAILURE'])
    aborted = len(
        last_builds.loc[last_builds['current_build_current_result'] == 'ABORTED'])
    unknows = total_rows - successes - failures - aborted

    statuses = [successes, failures, aborted, unknows]

    labels = ['SUCCESS',
              'FAILURE',
              'ABORTED',
              'UNKOWN']

    labels_with_amounts = list(
        map(
            lambda status, label: '{0} ({1})'.format(status, label),
            labels,
            statuses
        )
    )

    colors = [colors_map[label] for label in labels]

    layout = dict(
        title=go.layout.Title(text='Success Ratio for {0} {1} pipelines in the last {2} day(s) <br>(generated on {3})'.format(pipeline_type, branch, number_of_days, creation_time),
                              font=graph_title_font
                              ),
        paper_bgcolor=WHITE,
        plot_bgcolor=TRANSPARENT,
    )

    figure = {'data': [go.Pie(labels=labels_with_amounts, values=statuses, sort=False, marker=dict(colors=colors, line=pie_line_style))],
              'layout': layout
              }

    return figure
