import functools
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from dash_apps.lib.events_28d import events
from dash_apps.lib.filters import select
from style.theme import (TRANSPARENT, WHITE, colors_map, colorscale,
                         graph_title_font)


@functools.lru_cache(maxsize=128)
def get_fig(pipeline_type, project, days_in_past=14):

    df = select(events['df'], pipeline_type, project)
    creation_time = events['creation_time']
    creation_time_iso = events['creation_time_iso']

    time_interval = timedelta(days=days_in_past)

    builds_df = pd.DataFrame(
        df[df['current_build_scheduled_time'] > (
            creation_time_iso - time_interval).isoformat()]
        .sort_values(by='_ts')
        .drop_duplicates('build_tag', keep='last')
    )

    builds_df['Builds duration in minutes'] = builds_df['current_build_duration']/60000.0

    stats_dfs = {
        'SUCCESS': builds_df[builds_df['current_build_current_result'] == 'SUCCESS'],
        'FAILURE': builds_df[builds_df['current_build_current_result'] == 'FAILURE'],
        'ABORTED': builds_df[builds_df['current_build_current_result'] == 'ABORTED']
    }

    layout = dict(
        title=go.layout.Title(
            text='Duration distribution of {0} master pipelines over the last {1} days<br>(generated on {2})'.format(
                pipeline_type, days_in_past, creation_time),
            font=graph_title_font
        ),
        autosize=True,
        paper_bgcolor=WHITE,
        plot_bgcolor=TRANSPARENT,
        barmode='stack',
        xaxis=dict(title='Duration in minutes'),
        yaxis=dict(title='Number of pipelines'),
        marginal="rug"
    )

    data = [go.Histogram(
        name=status,
        x=stats_dfs[status]['Builds duration in minutes'],
        marker_color=colors_map[status], nbinsx=120) for status in ['SUCCESS', 'FAILURE', 'ABORTED']
    ]

    figure = {
        'data': data,
        'layout': layout
    }

    return figure
