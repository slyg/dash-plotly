import json
import os.path
import time
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash_app.lib.events_28d import events
from style.theme import TRANSPARENT, colorscale, graph_title_font

days_in_past = 14


def get_fig():

    # Load dataframe and contextual data

    df = events['df']
    creation_time = events['creation_time']
    creation_time_iso = events['creation_time_iso']

    # Number of hours we want to go back in
    hours_in_past = days_in_past * 24
    one_hour = timedelta(hours=1)

    reversed_last_hours = [(creation_time_iso - (i * one_hour)).isoformat()
                           for i in range(hours_in_past + 1)]

    last_hours = reversed_last_hours[::-1]

    # Generate hourly build reports from the dataframe

    def hour_builds(hour_df):
        return pd.DataFrame(
            hour_df
            .sort_values(by='stage_timestamp')
            .drop_duplicates('build_tag', keep='last')
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
            "has_data": 0 if total == 0 else 1,
            "failure_ratio": status_ratio(failures + aborted, total),
            "date": last_hours[i]
        })

    all_hours_stats = [hour_stats(i, x) for i, x in enumerate(builds)]

    stuff_df = pd.DataFrame.from_dict(all_hours_stats)
    stuff_df['hour'] = pd.to_datetime(
        stuff_df['date'], errors='coerce', infer_datetime_format=True).dt.hour
    stuff_df['day'] = pd.to_datetime(
        stuff_df['date'], errors='coerce', infer_datetime_format=True).dt.weekday_name

    failure_ratio_pivot_df = pd.pivot_table(
        stuff_df,
        values='failure_ratio',
        columns='hour',
        index=['day'],
        aggfunc=np.mean)

    failure_ratio_pivot_df.unstack(level=0)

    pipeline_count_pivot_df = pd.pivot_table(
        stuff_df,
        values='has_data',
        columns='hour',
        index=['day'],
        aggfunc=np.mean,
        fill_value=0)

    pipeline_count_pivot_df.unstack(level=0)

    # Make the days appear in the inverted week order
    days_of_the_week = ['Sunday', 'Saturday', 'Friday',
                        'Thursday', 'Wednesday', 'Tuesday', 'Monday']

    failure_ratio_pivot_df = failure_ratio_pivot_df.reindex(
        days_of_the_week, axis=0)

    pipeline_count_pivot_df = pipeline_count_pivot_df.reindex(
        days_of_the_week, axis=0)

    fig_title = "Heatmap of CI failures percentage average per hour per weekday over the last {0} days<br>(generated on {1})"\
                .format(days_in_past, str(creation_time))

    x_axis = failure_ratio_pivot_df.columns.tolist()
    y_axis = failure_ratio_pivot_df.index.tolist()
    z_axis = failure_ratio_pivot_df.values.tolist()
    has_data_axis = pipeline_count_pivot_df.values.tolist()

    dummy_x_axis = [x + 0.5 for x in x_axis]

    data = go.Heatmap(colorscale=colorscale['NegativelyOriented'],
                      hoverinfo='text',
                      hovertext=z_axis,
                      zhoverformat='.',
                      x=dummy_x_axis,
                      y=y_axis,
                      z=z_axis,
                      showscale=True,
                      colorbar={"title": 'Failure percentage', 'titleside': 'right'})

    raster = go.Heatmap(colorscale=colorscale['WhiteIfNoData'],
                        hoverinfo='skip',
                        hovertext=has_data_axis,
                        zhoverformat='.',
                        x=dummy_x_axis,
                        y=y_axis,
                        z=has_data_axis,
                        showscale=False,)

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
        paper_bgcolor=TRANSPARENT,
        plot_bgcolor=TRANSPARENT
    )

    figure = {'data': [data, raster],
              'layout': layout
              }

    return figure
