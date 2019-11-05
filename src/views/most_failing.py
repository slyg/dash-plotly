import json
import os.path
import time
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
from views.theme import colors_map, colorscale, graph_title_font

data_set_file = 'data/events_28d.pkl'


def get_fig():

    df = pd.read_pickle(data_set_file)
    creation_time = time.ctime(os.path.getctime(data_set_file))

    quantile = .75

    with open('data/events_28d.json') as json_file:
        data = json.load(json_file)
        branch = data['branch']

    days_in_past = 14

    failers = df[
        (df['current_build_current_result'] == 'FAILURE')
        | (df['current_build_current_result'] == 'ABORTED')
    ]['job_name'].value_counts().rename_axis('job_name').reset_index(name='counts')

    failers_qt = failers[failers['counts'] >
                         failers['counts'].quantile(quantile)]

    layout = dict(
        title=go.layout.Title(text='Top {0}% failing pipelines on {1} branch in the last {2} days<br>(generated on {3})'.format(
            round((1 - quantile) * 100), branch, days_in_past, creation_time),
            font=graph_title_font
        ),
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        bargap=0,
        yaxis=dict(
            automargin=True,
            ticksuffix=' —',
        ),
        xaxis=dict(
            type='log',
            title='Number of failed (failure and aborted) pipelines in the last {0} days (log axis)'.format(
                days_in_past),
        )
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
