import json
import os.path
import time
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from views.theme import colorscale, graph_title_font

# Load dataframe and contextual data

data_set_file = 'data/heatmap.pkl'
df = pd.read_pickle(data_set_file)

DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
DATE_FORMAT_UTC = '%Y-%m-%dT%H:%M:%S.%f'
with open('data/heatmap.json') as json_file:
    data = json.load(json_file)
    last_hours = data['last_hours']
    now = datetime.strptime(data['now'], DATE_FORMAT)

# Generate hourly build reports from the dataframe


def hour_builds(hour_df):
    return pd.DataFrame(
        hour_df
        .sort_values(by='stage_timestamp')
        .drop_duplicates('job_name', keep='last')
    )


def hour_df(frame, hour_number):
    return frame[
        (frame['stage_timestamp'] > last_hours[hour_number])
        & (frame['stage_timestamp'] < last_hours[hour_number + 1])
    ]


builds = [hour_builds(hour_df(df, hour_number))
          for hour_number in list(range(len(last_hours) - 1))]


def status_ratio(status, total):
    return 100 if total == 0 else round(status/total * 100)


def hour_stats(i, current_build):
    successes = len(
        current_build.loc[df['current_build_current_result'] == 'SUCCESS'])
    failures = len(
        current_build.loc[df['current_build_current_result'] == 'FAILURE'])
    aborted = len(
        current_build.loc[df['current_build_current_result'] == 'ABORTED'])

    total = successes + failures + aborted

    return ({
        "failure_ratio": status_ratio(failures + aborted, total),
        "date": last_hours[i]
    })


all_hours_stats = [hour_stats(i, x) for i, x in enumerate(builds)]

stuff_df = pd.DataFrame.from_dict(all_hours_stats)
stuff_df['hour'] = pd.to_datetime(
    stuff_df['date'], errors='coerce', infer_datetime_format=True).dt.hour
stuff_df['day'] = pd.to_datetime(
    stuff_df['date'], errors='coerce', infer_datetime_format=True).dt.weekday_name

pivot_stuff_df = pd.pivot_table(
    stuff_df,
    values='failure_ratio',
    columns='hour',
    index=['day'],
    aggfunc=np.mean)

pivot_stuff_df.unstack(level=0)

# Make the days appear in the inverted week order
days_of_the_week = ['Sunday', 'Saturday', 'Friday',
                    'Thursday', 'Wednesday', 'Tuesday', 'Monday']
pivot_stuff_df = pivot_stuff_df.reindex(days_of_the_week, axis=0)

fig_title = "Heatmap of CI failures percentage average per hour per weekday over the last 28 days<br>(generated on {0})"\
            .format(str(now.ctime()))

x_axis = pivot_stuff_df.columns.tolist()
y_axis = pivot_stuff_df.index.tolist()
z_axis = pivot_stuff_df.values.tolist()

dummy_x_axis = [x + 0.5 for x in x_axis]

data = go.Heatmap(colorscale=colorscale['WhiteToRed'],
                  hoverinfo='text',
                  hovertext=z_axis,
                  zhoverformat='.',
                  x=dummy_x_axis,
                  y=y_axis,
                  z=z_axis)

layout = dict(
    title=go.layout.Title(text=fig_title, font=graph_title_font),
    xaxis=dict(
        tickangle=-90,
        tickmode='array',
        tickvals=x_axis,
        ticktext=['{0}:00'.format(x) for x in x_axis]
    ),
    margin=dict(
        pad=0
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)


figure = {'data': [data],
          'layout': layout
          }
