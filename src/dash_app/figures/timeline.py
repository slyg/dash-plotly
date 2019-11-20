import functools
import json
import os.path
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from dash_app.lib.filters import select
from style.theme import TRANSPARENT, WHITE, colors_map, graph_title_font

data_set_file = 'data/events_180d.pkl'


@functools.lru_cache(maxsize=128)
def get_fig(pipeline_type, project):

    df = pd.DataFrame(
        pd.read_pickle(data_set_file)
        .sort_values(by='stage_timestamp')
        .drop_duplicates('build_tag', keep='last')
    )

    df = select(df, pipeline_type, project)

    creation_time = time.ctime(os.path.getctime(data_set_file))

    with open('data/events_180d.json') as json_file:
        data = json.load(json_file)
        days_in_past = int(data['days_in_past'])
        last_days = data['last_days']

    def day_stats(date_index):
        day_frame = df[
            (df['stage_timestamp'] >= last_days[date_index])
            & (df['stage_timestamp'] < last_days[date_index+1])
        ]

        total_rows = len(day_frame)
        SUCCESS = len(
            day_frame.loc[df['current_build_current_result'] == 'SUCCESS'])
        FAILURE = len(
            day_frame.loc[df['current_build_current_result'] == 'FAILURE'])
        ABORTED = len(
            day_frame.loc[df['current_build_current_result'] == 'ABORTED'])
        UNKNOWN = total_rows - SUCCESS - FAILURE - ABORTED

        return ({
            "stats": [SUCCESS, FAILURE, ABORTED, UNKNOWN],
            "stats_labels": ['SUCCESS', 'FAILURE', 'ABORTED', 'UNKNOWN'],
            "date": {"from": last_days[date_index], "to": last_days[date_index+1]}
        })

    all_days_stats = [day_stats(date_index)
                      for date_index in list(range(len(last_days) - 1))]

    def ratio_for_index(l, idx):
        return [0 if sum(item['stats']) == 0 else item['stats'][idx]/sum(item['stats'])*100 for item in l]

    def get_rounded_labels(l, k):
        return ['{0}%'.format(round(item)) for item in l[k]]

    horizontal_axis_labels = [stats['date']['from']
                              for stats in all_days_stats]

    data = {
        'SUCCESS': ratio_for_index(all_days_stats, 0),
        'FAILURE':  ratio_for_index(all_days_stats, 1),
        'ABORTED':   ratio_for_index(all_days_stats, 2),
    }

    rounded_labels = {
        'SUCCESS': get_rounded_labels(data, 'SUCCESS'),
        'FAILURE':  get_rounded_labels(data, 'FAILURE'),
        'ABORTED':   get_rounded_labels(data, 'ABORTED'),
    }

    def get_bar(dimension):
        return go.Bar(name=dimension.capitalize(),
                      x=horizontal_axis_labels,
                      y=data[dimension],
                      marker_color=colors_map[dimension],
                      hovertext=rounded_labels[dimension],
                      hoverinfo='text')

    layout = dict(
        title=go.layout.Title(text='Failure percentage of CI for {0} master pipelines over the last {1} days<br>(generated on {2})'.format(pipeline_type, days_in_past, creation_time),
                              font=graph_title_font
                              ),
        barmode='stack',
        bargap=0,
        paper_bgcolor=WHITE,
        plot_bgcolor=TRANSPARENT,
        xaxis=dict(
            tickangle=-90,
            nticks=round(days_in_past/4),
            rangeselector=dict(
                buttons=list([
                    dict(step='all'),
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date',
        )
    )

    data = [get_bar(status) for status in ['ABORTED', 'FAILURE', 'SUCCESS']]

    figure = {
        'data': data,
        'layout': layout
    }

    return figure
