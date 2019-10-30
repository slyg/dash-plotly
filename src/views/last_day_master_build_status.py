import os.path
import time

import pandas as pd
import plotly.graph_objects as go
from views.theme import colors_map, graph_title_font

data_set_file = 'data/last_day_master_build_status.pkl'

last_builds = pd.read_pickle(data_set_file)
creation_time = time.ctime(os.path.getctime(data_set_file))

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
    title=go.layout.Title(text='Success Ratio for master builds initiated in the last 24h <br>(gen: {0})'.format(creation_time),
                          font=graph_title_font
                          )
)

figure = {'data': [go.Pie(labels=labels_with_amounts, values=statuses)],
          'layout': layout
          }
