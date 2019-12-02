import functools
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from dash_apps.lib.events_28d import events
from dash_apps.lib.filters import select
from style.theme import (TRANSPARENT, WHITE, colors_map, colorway,
                         graph_title_font, pie_line_style)


@functools.lru_cache(maxsize=128)
def get_fig(pipeline_type, project, days_in_past=14):

    df = select(events['df'], pipeline_type, project)
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
            title='Number of failed steps'
        ),
        colorway=colorway['GovUkColours'],
        height=800,
    )

    pie = go.Pie(labels=labels,
                 values=values,
                 hole=.4,
                 marker=dict(line=pie_line_style)
                 )

    figure = {
        'data': [pie],
        'layout': layout
    }

    return figure
