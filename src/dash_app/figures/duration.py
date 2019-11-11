import json
import os.path
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from style.theme import colors_map, colorscale, graph_title_font

data_set_file = 'data/events_28d.pkl'


def get_fig():

    df = pd.read_pickle(data_set_file)
    creation_time = time.ctime(os.path.getctime(data_set_file))
    creation_time_iso = datetime.strptime(
        creation_time, "%a %b %d %H:%M:%S %Y")

    days_in_past = 7

    time_interval = timedelta(days=days_in_past)

    builds_df = pd.DataFrame(
        df[df['current_build_scheduled_time'] > (
            creation_time_iso - time_interval).isoformat()]
        .sort_values(by='_ts')
        .drop_duplicates('correlation_id', keep='last')
    )

    builds_df['Succeeding builds duration in minutes'] = builds_df['current_build_duration']/60000.0

    stats_dfs = {
        'SUCCESS': builds_df[builds_df['current_build_current_result'] == 'SUCCESS'],
        'FAILURE': builds_df[builds_df['current_build_current_result'] == 'FAILURE'],
        'ABORTED': builds_df[builds_df['current_build_current_result'] == 'ABORTED']
    }

    layout = dict(
        title=go.layout.Title(
            text='Pipelines duration distribution in minutes the last {0} days<br>(generated on {1})'.format(
                days_in_past, creation_time),
            font=graph_title_font
        ),
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
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
