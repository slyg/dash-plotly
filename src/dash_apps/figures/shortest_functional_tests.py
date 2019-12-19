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
    creation_time_iso = events['creation_time_iso']
    branch = events['branch']

    time_interval = timedelta(days=days_in_past)

    # Select functionalTest and smoketest (step before) events
    data_df = pd.DataFrame(
        df[((df['current_step_name'] == 'functionalTest:aat') | (df['current_step_name'] == 'smoketest:aat'))
            & (df['current_build_current_result'] == 'SUCCESS')
            & (df['current_build_scheduled_time'] > (creation_time_iso - time_interval).isoformat())
           ]
    )

    # Select latest jobs per job name and build if
    df_sorted = data_df\
        .sort_values(['job_name', 'build_id'])\
        .drop_duplicates(['job_name', 'build_id', 'current_step_name'])

    # Isolate each type of event in separate dataframe
    #
    # The assumption is that the smokeTests:aat endings provide the start time
    # of the functionalTest:aat step, as it is programatically the next step.
    #
    # This is a workaround to guess the duration of the functionalTest:aat step.

    df_smoke = (df_sorted[df_sorted['current_step_name'] == 'smoketest:aat'])
    df_func_tests = (
        df_sorted[df_sorted['current_step_name'] == 'functionalTest:aat'])

    # Simplify the dataframe so that we keep the job_name and schedule time
    df_smoke_simple = df_smoke[['job_name', 'stage_timestamp']]\
        .drop_duplicates('job_name')\
        .reset_index(drop=True)\
        .sort_values(['job_name'])

    df_func_tests_simple = df_func_tests[['job_name', 'stage_timestamp']]\
        .drop_duplicates('job_name')\
        .reset_index(drop=True)\
        .sort_values(['job_name'])

    # Recreate a dataframe with step start (previous step end) and step end

    df3 = pd.merge(df_smoke_simple, df_func_tests_simple, on="job_name")
    df4 = df3.rename(
        columns={"stage_timestamp_x": "start", "stage_timestamp_y": "end"})

    # Compute time difference

    def step_time_duration(start, end):
        b = datetime.strptime(end, "%Y-%m-%dT%H:%M:%SZ")
        a = datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
        return int((b - a).total_seconds())

    df4['time_diff_in_s'] = df4.apply(
        lambda x: step_time_duration(x.start, x.end), axis=1)

    # Filter negative (aka invalid) values
    #
    # Some smokeTests:aat step event timestamp are timed AFTER the actual following functionalTests:aat
    # which is very odd and doesn't bring a lot of confidence in the data source.
    # However, the "cleaned" results seem pretty consistent with the observed pipelines

    df5 = (df4[
        (df4['time_diff_in_s'] > 0)
        & (df4['time_diff_in_s'] < 500)
    ]).head(10)

    report = df5[['job_name', 'time_diff_in_s']].sort_values(
        by='time_diff_in_s', ascending=False).reset_index(drop=True)

    layout = dict(
        title=go.layout.Title(text='Shortest latest AAT functional tests duration in {0} pipelines on {1} branch<br>(generated on {2})'.format(
            pipeline_type, branch, creation_time),
            font=graph_title_font
        ),
        autosize=True,
        paper_bgcolor=WHITE,
        plot_bgcolor=TRANSPARENT,
        bargap=0,
        yaxis=dict(
            automargin=True,
            ticksuffix=' —',
        ),
        xaxis=dict(
            title='Time in seconds',
        ),
        height=(len(report) + 10) * 20,
    )

    def get_bar(data_frame):
        return go.Bar(y=data_frame['job_name'],
                      x=data_frame['time_diff_in_s'],
                      width=1,
                      orientation='h',
                      marker={'color': data_frame['time_diff_in_s'],
                              'colorscale': colorscale['InvertedRainbow']}
                      )

    data = [get_bar(report)]

    figure = {
        'data': data,
        'layout': layout
    }

    return figure
