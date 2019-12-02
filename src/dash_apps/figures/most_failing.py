import functools
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from dash_apps.lib.events_28d import events
from dash_apps.lib.filters import select
from style.theme import (TRANSPARENT, WHITE, colors_map, colorscale,
                         graph_title_font)

max_results = 50


@functools.lru_cache(maxsize=128)
def get_fig(pipeline_type, project, days_in_past=14):

    df = select(events['df'], pipeline_type, project)
    creation_time = events['creation_time']
    branch = events['branch']

    failers = df[
        (df['current_build_current_result'] == 'FAILURE')
        | (df['current_build_current_result'] == 'ABORTED')
    ]['job_name'].value_counts().rename_axis('job_name').reset_index(name='counts')

    top_failers = failers.head(max_results)

    layout = dict(
        title=go.layout.Title(text='Most frequent failing pipelines on {0} branch for {1} pipelines in the last {2} days<br>(generated on {3})'.format(
            branch, pipeline_type, days_in_past, creation_time),
            font=graph_title_font
        ),
        autosize=True,
        paper_bgcolor=WHITE,
        plot_bgcolor=TRANSPARENT,
        bargap=0,
        yaxis=dict(
            automargin=True,
            autorange="reversed",
            ticksuffix=' —',
        ),
        xaxis=dict(
            title='Number of failed (failure and aborted) pipelines'
        ),
        height=(len(top_failers) + 10) * 20,
    )

    def get_bar(data_frame):
        return go.Bar(y=data_frame['job_name'],
                      x=data_frame['counts'],
                      width=1,
                      orientation='h',
                      marker={'color': data_frame['counts'],
                              'colorscale': colorscale['YellowToRed']}
                      )

    data = [get_bar(top_failers)]

    figure = {
        'data': data,
        'layout': layout
    }

    return figure
