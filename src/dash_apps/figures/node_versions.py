import functools
import os.path as path
import re
import time

import pandas as pd
import plotly.graph_objects as go
from style.theme import (TRANSPARENT, WHITE, colorway, graph_title_font,
                         pie_line_style)

data_src_file = 'data/node-versions.csv'
df = pd.read_csv(data_src_file)
creation_time = time.ctime(path.getctime(data_src_file))


@functools.lru_cache(maxsize=128)
def get_fig():

    unique_versions = list(df['version'].unique())
    unique_versions.sort()

    unique_simple_versions = list(
        ["v." + re.findall(r'\d+', v)[0] for v in unique_versions])

    unique_simple_versions_parents = list(
        ["All versions" for _ in dict.fromkeys(unique_simple_versions)])

    projects_names = list(df['name'])
    versions = list(df['version'])

    labels = list(dict.fromkeys(unique_simple_versions)) + \
        unique_versions + projects_names
    parents = unique_simple_versions_parents + unique_simple_versions + versions

    print(labels)
    print(parents)

    layout = dict(
        title=go.layout.Title(text='NodeJS versions in use<br>(Generated on {})'.format(creation_time),
                              font=graph_title_font
                              ),
        paper_bgcolor=WHITE,
        plot_bgcolor=TRANSPARENT,
        colorway=colorway['CurrentToDeprecated'],
        height=600,
    )

    return {
        'data': [
            go.Treemap(
                labels=labels,
                parents=parents,
                textposition="middle center",
                tiling=dict(
                    packing="slice",
                    squarifyratio=3,
                ),
                marker=dict(
                    line=dict(width=0),
                ),
            )],
        'layout': layout
    }
