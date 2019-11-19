import json
import os.path
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from dash_app.lib.events_28d import events
from dash_app.lib.nightly import select
from style.theme import TRANSPARENT, colors_map, colorscale, graph_title_font

data_set_file = 'data/events_28d.pkl'


def get_fig(selection):

    df = select(selection, events['df'])
    creation_time = events['creation_time']
    creation_time_iso = events['creation_time_iso']
    branch = events['branch']

    time_interval = timedelta(minutes=15)
    days_in_past = 14
    number_of_intervals = round(
        days_in_past * 24 * 4)  # 15 min slots over 24h
    reversed_intervals = [(creation_time_iso - (i * time_interval)).isoformat()
                          for i in range(number_of_intervals + 1)]
    intervals = reversed_intervals[::-1]

    builds_df = pd.DataFrame(
        df
        .sort_values(by='stage_timestamp')
        .drop_duplicates('build_tag', keep='last')
    )

    def get_status_for(status, from_, to_):
        return len(builds_df.loc[
            (builds_df['current_build_current_result'] == status)
            & (builds_df['current_build_scheduled_time'] > from_)
            & (builds_df['current_build_scheduled_time'] < to_)
        ])

    def interval_stats(from_, to_):

        success = get_status_for('SUCCESS', from_, to_)
        failure = get_status_for('FAILURE', from_, to_)
        aborted = get_status_for('ABORTED', from_, to_)
        total_count = success + failure + aborted

        return ({
            "failure_ratio": 1 if total_count == 0 else (failure + aborted) / total_count,
            "count": total_count,
            "date": {
                "from": from_,
                "to": to_
            }
        })

    all_intervals_stats = [interval_stats(
        intervals[i-1], intervals[i]) for i, x in enumerate(intervals)]

    layout = dict(
        title=go.layout.Title(text='CI {0} pipelines counts and failure percentage over the last {1} days<br>(generated on {2})'.format(branch, days_in_past, creation_time),
                              font=graph_title_font
                              ),
        bargap=0,
        height=500,
        paper_bgcolor=TRANSPARENT,
        plot_bgcolor=TRANSPARENT,
        yaxis=dict(
            title='Count',
            nticks=4),
        xaxis=dict(
            tickangle=-90,
            rangeselector=dict(
                buttons=list([
                    dict(step='all'),
                    dict(count=7,
                         label='7d',
                         step='day',
                         active=True),
                    dict(count=3,
                         label='3d',
                         step='day',
                         active=True),
                    dict(count=24,
                         label='1d',
                         step='hour'),
                    dict(count=6,
                         label='6h',
                         step='hour')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            range=[(creation_time_iso - timedelta(days=7)
                    ).isoformat(), creation_time_iso.isoformat()],
            type='date'
        )
    )
    graph_df = pd.DataFrame({
        'count': [item['count'] for item in all_intervals_stats],
        'failure_percentage': [round(100 * item['failure_ratio']) for item in all_intervals_stats],
        'xaxis_labels': [stats['date']['from'] for stats in all_intervals_stats]
    })

    data = [go.Bar(name='count',
                   x=graph_df['xaxis_labels'],
                   y=graph_df['count'],
                   marker={'color': graph_df['failure_percentage'],
                           'colorscale': colorscale['NegativelyOriented'],
                           'colorbar': {'title': 'Failure percentage', 'titleside': 'right'},
                           'showscale': True},
                   hovertext=graph_df['failure_percentage'].apply(
                       lambda x: '{0}%'.format(x)),
                   hoverinfo='text')]

    figure = {
        'data': data,
        'layout': layout
    }

    return figure
