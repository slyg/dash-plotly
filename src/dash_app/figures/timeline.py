import json
import os.path
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from style.theme import colors_map, graph_title_font

data_set_file = 'data/events_180d.pkl'

df = pd.read_pickle(data_set_file)
creation_time = time.ctime(os.path.getctime(data_set_file))


def get_fig():

    with open('data/events_180d.json') as json_file:
        data = json.load(json_file)
        days_in_past = int(data['days_in_past'])
        last_days = data['last_days']

    def day_builds(week_df):
        return pd.DataFrame(
            week_df
            .sort_values(by='stage_timestamp')
            .drop_duplicates('correlation_id', keep='last')
        )

    def day_df(frame, day_number):
        return frame[
            (frame['stage_timestamp'] > last_days[day_number])
            & (frame['stage_timestamp'] < last_days[day_number + 1])
        ]

    builds = [day_builds(day_df(df, day_number))
              for day_number in list(range(len(last_days) - 1))]

    def day_stats(i, current_build):
        total_rows = len(current_build)
        SUCCESS = len(
            current_build.loc[df['current_build_current_result'] == 'SUCCESS'])
        FAILURE = len(
            current_build.loc[df['current_build_current_result'] == 'FAILURE'])
        ABORTED = len(
            current_build.loc[df['current_build_current_result'] == 'ABORTED'])
        UNKNOWN = total_rows - SUCCESS - FAILURE - ABORTED

        return ({
            "stats": [SUCCESS, FAILURE, ABORTED, UNKNOWN],
            "stats_labels": ['SUCCESS', 'FAILURE', 'ABORTED', 'UNKNOWN'],
            "date": {"from": last_days[i], "to": last_days[i+1]}
        })

    all_days_stats = [day_stats(i, x) for i, x in enumerate(builds)]

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
        title=go.layout.Title(text='Failure percentage of CI master pipelines over the last {0} days<br>(generated on {1})'.format(days_in_past, creation_time),
                              font=graph_title_font
                              ),
        barmode='stack',
        bargap=0,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
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
