import functools
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from dash_app.lib.events_28d import events
from dash_app.lib.nightly import select
from style.theme import TRANSPARENT, colors_map, colorscale, graph_title_font

days_in_past = 14


@functools.lru_cache(maxsize=128)
def get_fig(selection):

    df = select(selection, events['df'])
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
        title=go.layout.Title(text='Top failing steps on {0} branch for {1} pipelines in the last {2} days<br>(generated on {3})'.format(
            branch, selection, days_in_past, creation_time),
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
            type='category',
            size=10,
        ),
        xaxis=dict(
            title='Number of failed pipeline'
        ),
        height=600,
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
