import json
import os.path
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from style.theme import TRANSPARENT, colors_map, colorscale, graph_title_font

data_set_file = 'data/events_28d.pkl'


def get_fig():

    df = pd.read_pickle(data_set_file)
    creation_time = time.ctime(os.path.getctime(data_set_file))

    with open('data/events_28d.json') as json_file:
        data = json.load(json_file)
        branch = data['branch']

    days_in_past = 14

    last_failed_builds_penultimate_step = df[(df['current_build_current_result'] == 'FAILURE')
                                             & (df['current_step_name'] != 'Pipeline Failed')]\
        .sort_values('stage_timestamp')\
        .drop_duplicates('build_tag', keep='last')

    data = last_failed_builds_penultimate_step\
        .sort_values(by='job_name')\
        .current_step_name.value_counts()

    labels = list(data.index[0:len(data.index)])
    values = list(data.values)

    layout = dict(
        title=go.layout.Title(text='Failing steps on {0} branch in the last {1} days<br>(generated on {2})'.format(
            branch, days_in_past, creation_time),
            font=graph_title_font
        ),
        autosize=True,
        paper_bgcolor=TRANSPARENT,
        plot_bgcolor=TRANSPARENT,
        bargap=0,
        yaxis=dict(
            automargin=True,
            autorange="reversed",
            ticksuffix=' —',
        ),
        xaxis=dict(
            type='log',
            title='Number of failed (failure and aborted) pipelines in the last {0} days (log axis)'.format(
                days_in_past),
        )
    )

    def get_bar(data_frame):
        return go.Bar(y=labels,
                      x=values,
                      width=1,
                      orientation='h',
                      marker={'color': values,
                              'colorscale': colorscale['YellowToRed']}
                      )

    data = [get_bar(data)]

    figure = {
        'data': data,
        'layout': layout
    }

    return figure
