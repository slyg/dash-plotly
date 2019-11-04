import json
import os.path
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from views.theme import colors_map, colorscale, graph_title_font

data_set_file = 'data/events_28d.pkl'

df = pd.read_pickle(data_set_file)
creation_time = time.ctime(os.path.getctime(data_set_file))
creation_time_iso = datetime.strptime(creation_time, "%a %b %d %H:%M:%S %Y")


with open('data/events_28d.json') as json_file:
    data = json.load(json_file)
    days_in_past = data['days_in_past']
    branch = data['branch']

time_interval = timedelta(minutes=5)
number_of_days = 14
number_of_intervals = round(
    number_of_days * 24 * 12)  # 5 min slots over 24h
max_past_date = (creation_time_iso - (number_of_intervals + 1) * time_interval)
reversed_intervals = [(creation_time_iso - (i * time_interval)).isoformat()
                      for i in range(number_of_intervals + 1)]
intervals = reversed_intervals[::-1]

sub_df = df[df['current_build_scheduled_time'] > str(intervals[0])]


def interval_df(df, interval_number):
    return df[
        (df['stage_timestamp'] > intervals[interval_number])
        & (df['stage_timestamp'] < intervals[interval_number + 1])
    ]


def interval_builds(df):
    return pd.DataFrame(
        df
        .sort_values(by='stage_timestamp')
        .drop_duplicates('id', keep='last')
    )


builds = [interval_builds(interval_df(sub_df, n))
          for n in list(range(len(intervals) - 1))]


def interval_stats(i, current_build):

    success = len(
        current_build.loc[df['current_build_current_result'] == 'SUCCESS'])
    failure = len(
        current_build.loc[
            (df['current_build_current_result'] == 'FAILURE')
            | (df['current_build_current_result'] == 'ABORTED')
        ])
    total_count = success + failure

    return ({
        "failure_ratio": 1 if total_count == 0 else failure / total_count,
        "count": total_count,
        "date": {
            "from": intervals[i],
            "to": intervals[i+1]
        }
    })


all_intervals_stats = [interval_stats(i, x) for i, x in enumerate(builds)]

layout = dict(
    title=go.layout.Title(text='CI {0} pipelines counts and failure rates over the last {1} days<br>(generated on {2})'.format(branch, number_of_days, creation_time),
                          font=graph_title_font
                          ),
    bargap=0,
    height=600,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
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
