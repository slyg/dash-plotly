import dash_apps.figures.cve_suppressions_most_frequent as cve_suppressions_most_frequent
import dash_apps.figures.cve_suppressions_per_team as cve_suppressions_per_team
import dash_apps.figures.js_apps_checks as js_apps_checks
import dash_core_components as dcc
import dash_html_components as html
from dash_apps.components.header import getHeader
from dash_apps.components.layout import layout
from style.theme import BRAND


def set_layout(app):
    header = [getHeader(app)]
    body = [
        html.Div(className='col col-12 col-xl-6 my-3',
                 children=[
                     html.Div(children=[
                         dcc.Loading(color=BRAND, children=[
                                     dcc.Graph(
                                         id='cve_suppressions_most_frequent',
                                         figure=cve_suppressions_most_frequent.get_fig()
                                     )
                                     ])
                     ]),
                 ]),
        html.Div(className='col col-12 col-xl-6 my-3',
                 children=[
                     html.Div(children=[
                         dcc.Loading(color=BRAND, children=[
                                     dcc.Graph(
                                         id='cve_suppressions_per_team',
                                         figure=cve_suppressions_per_team.get_fig()
                                     )
                                     ])
                     ]),
                 ]),
        html.Div(className='col col-12 col-xl-6 my-3',
                 children=[
                     html.Div(children=[
                         dcc.Loading(color=BRAND, children=[
                                     dcc.Graph(
                                         id='js_apps_checks',
                                         figure=js_apps_checks.get_fig()
                                     )
                                     ])
                     ]),
                 ]),
    ]

    app.layout = layout(header, body)
