import json
import os.path
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from dash_app.lib.events_28d import events
from style.theme import (TRANSPARENT, WHITE, colors_map, colorway,
                         graph_title_font)

days_in_past = 14


def get_fig():

    df = events['df']
    creation_time = events['creation_time']
    branch = events['branch']

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
        title=go.layout.Title(text='Top failing steps on {0} branch in the last {1} days<br>(generated on {2})'.format(
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
            title='Number of failed steps'
        ),
        colorway=colorway['HueGradient'],
        height=800,
    )

    pie = go.Pie(labels=labels,
                 values=values,
                 hole=.4,
                 marker=dict(line=dict(color=WHITE, width=1))
                 )

    figure = {
        'data': [pie],
        'layout': layout
    }

    return figure
