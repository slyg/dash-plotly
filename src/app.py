import os.path
import time

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

data_set_file = 'data/24h-master-build-status.pkl'

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

colors_map = {
    'ABORTED': '#FF8C11',
    'FAILURE': '#E55934',
    'SUCCESS': '#7CCE77',
    'UNKOWN':  '#CCCCCC'
}

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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [go.Pie(labels=labels_with_amounts, values=statuses)],
            'layout': {
                'title': 'Success Ratio for master builds initiated in the last 24h <br>(gen: {0})'.format(creation_time)
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host="0.0.0.0")
