import os.path as path
import time

import pandas as pd
import plotly.graph_objects as go
from style.theme import (TRANSPARENT, WHITE, colorscale, graph_title_font,
                         pie_line_style)

data_src_file = 'data/cve_suppressions.csv'
df = pd.read_csv(data_src_file)
creation_time = time.ctime(path.getctime(data_src_file))


def get_fig():
    data = df.groupby('CVE')['Team']\
        .nunique()\
        .sort_values(ascending=True)

    report_df = pd.DataFrame({
        'CVE': data.index,
        'Count': data.values
    })

    report_df = report_df[report_df['Count']
                          > 2].sort_values(by=['Count', 'CVE'])

    layout = dict(
        title=go.layout.Title(text='Most frequent CVE suppressions<br>(Generated on {})'.format(creation_time),
                              font=graph_title_font
                              ),
        autosize=True,
        paper_bgcolor=WHITE,
        plot_bgcolor=TRANSPARENT,
        bargap=0,
        xaxis=dict(
            automargin=True,
            ticksuffix=' —',
            dtick=1,
            tickangle=-90,
        ),
        yaxis=dict(
            title='Number of occurrence',
        ),
        height=600,
    )

    return {'data': [go.Bar(y=report_df['Count'],
                            x=report_df['CVE'],
                            width=1,
                            orientation='v',
                            marker={'color': report_df['Count'],
                                    'colorscale': colorscale['Rainbow']}
                            )],
            'layout': layout
            }
