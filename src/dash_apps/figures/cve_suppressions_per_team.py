import os.path as path
import time

import pandas as pd
import plotly.graph_objects as go
from style.theme import (TRANSPARENT, WHITE, colorway, graph_title_font,
                         pie_line_style)

data_src_file = 'data/cve_suppressions.csv'
df = pd.read_csv(data_src_file)
creation_time = time.ctime(path.getctime(data_src_file))


def get_fig():

    data = df.groupby('Team')['CVE'].nunique().sort_values(ascending=False)

    labels = data.index
    values = data.values

    layout = dict(
        title=go.layout.Title(text='CVE suppressions count per team<br>(Generated on {})'.format(creation_time),
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
