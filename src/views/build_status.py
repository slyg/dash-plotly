import os.path
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from views.theme import colors_map, graph_title_font

data_set_file = 'data/events_28d.pkl'

number_of_hours = 24

df = pd.read_pickle(data_set_file)
creation_time = time.ctime(os.path.getctime(data_set_file))
creation_time_iso = datetime.strptime(creation_time, "%a %b %d %H:%M:%S %Y")
one_hour = timedelta(hours=1)
max_past_date = (creation_time_iso - (number_of_hours * one_hour)).isoformat()

last_builds = df[df['stage_timestamp'] > max_past_date]
last_builds = last_builds.sort_values(
    by='stage_timestamp').drop_duplicates('id', keep='last')

total_rows = len(last_builds)
successes = len(
    last_builds.loc[last_builds['current_build_current_result'] == 'SUCCESS'])
failures = len(
    last_builds.loc[last_builds['current_build_current_result'] == 'FAILURE'])
aborted = len(
    last_builds.loc[last_builds['current_build_current_result'] == 'ABORTED'])
unknows = total_rows - successes - failures - aborted
success_ratio = round(successes/total_rows * 100)

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
    title=go.layout.Title(text='Success Ratio for master CI pipelines initiated in the last {0} hours <br>(generated on {1})'.format(number_of_hours, creation_time),
                          font=graph_title_font
                          ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

figure = {'data': [go.Pie(labels=labels_with_amounts, values=statuses, marker=dict(colors=colors))],
          'layout': layout
          }
