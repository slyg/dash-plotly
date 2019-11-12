import json
import os.path
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from dash_app.lib.events_28d import events
from style.theme import TRANSPARENT, colors_map, colorscale, graph_title_font

days_in_past = 14


def get_fig():

    df = events['df']
    creation_time = events['creation_time']
    creation_time_iso = events['creation_time_iso']

    time_interval = timedelta(days=days_in_past)

    builds_df = pd.DataFrame(
        df[df['current_build_scheduled_time'] > (
            creation_time_iso - time_interval).isoformat()]
        .sort_values(by='_ts')
        .drop_duplicates('build_tag', keep='last')
    )

    builds_df['Succeeding builds duration in minutes'] = builds_df['current_build_duration']/60000.0

    stats_dfs = {
        'SUCCESS': builds_df[builds_df['current_build_current_result'] == 'SUCCESS'],
        'FAILURE': builds_df[builds_df['current_build_current_result'] == 'FAILURE'],
        'ABORTED': builds_df[builds_df['current_build_current_result'] == 'ABORTED']
    }

    layout = dict(
        title=go.layout.Title(
            text='Pipelines duration distribution in minutes over the last {0} days<br>(generated on {1})'.format(
                days_in_past, creation_time),
            font=graph_title_font
        ),
        autosize=True,
        paper_bgcolor=TRANSPARENT,
        plot_bgcolor=TRANSPARENT,
        barmode='stack',
        xaxis=dict(title='Duration in minutes'),
        yaxis=dict(title='Number of pipelines'),
        marginal="rug"
    )

    data = [go.Histogram(
        name=status,
        x=stats_dfs[status]['Succeeding builds duration in minutes'],
        marker_color=colors_map[status], nbinsx=100) for status in ['SUCCESS', 'FAILURE', 'ABORTED']
    ]

    figure = {
        'data': data,
        'layout': layout
    }

    return figure
