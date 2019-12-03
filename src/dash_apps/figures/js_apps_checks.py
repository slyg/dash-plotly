import os.path as path
import time

import pandas as pd
import plotly.graph_objects as go
from style.theme import (TRANSPARENT, WHITE, colorway, graph_title_font,
                         pie_line_style)

data_src_file = 'data/js_apps_sec_checks.csv'
df = pd.read_csv(data_src_file)
creation_time = time.ctime(path.getctime(data_src_file))


def get_fig():

    sums = df[df.columns[1:]].sum()
    labels = list(sums.index)
    values = list(sums.values)

    layout = dict(
        title=go.layout.Title(text='Javascript/nodejs projects security checks<br>(Generated on {})'.format(creation_time),
                              font=graph_title_font
                              ),
        paper_bgcolor=WHITE,
        plot_bgcolor=TRANSPARENT,
        colorway=colorway['GovUkColours'],
        height=600,
    )

    return {'data': [go.Pie(labels=labels, values=values, sort=False, marker=dict(line=pie_line_style))],
            'layout': layout
            }
