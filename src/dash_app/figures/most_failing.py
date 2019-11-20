import functools
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from dash_app.lib.events_28d import events
from dash_app.lib.nightly import select
from style.theme import (TRANSPARENT, WHITE, colors_map, colorscale,
                         graph_title_font)

days_in_past = 14
quantile = .75


@functools.lru_cache(maxsize=128)
def get_fig(selection):

    df = select(selection, events['df'])
    creation_time = events['creation_time']
    branch = events['branch']

    failers = df[
        (df['current_build_current_result'] == 'FAILURE')
        | (df['current_build_current_result'] == 'ABORTED')
    ]['job_name'].value_counts().rename_axis('job_name').reset_index(name='counts')

    failers_qt = failers[failers['counts'] >
                         failers['counts'].quantile(quantile)]

    layout = dict(
        title=go.layout.Title(text='Top {0}% Failing pipelines on {1} branch for {2} pipelines in the last {3} days<br>(generated on {3})'.format(
            round((1 - quantile) * 100), branch, selection, days_in_past, creation_time),
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
        height=800,
    )

    def get_bar(data_frame):
        return go.Bar(y=data_frame['job_name'],
                      x=data_frame['counts'],
                      width=1,
                      orientation='h',
                      marker={'color': data_frame['counts'],
                              'colorscale': colorscale['YellowToRed']}
                      )

    data = [get_bar(failers_qt)]

    figure = {
        'data': data,
        'layout': layout
    }

    return figure
