import dash_core_components as dcc
import dash_html_components as html
from style.theme import BRAND, WHITE_ALPHA_8


def getHeader(app, filters=None):
    return html.Nav(className='navbar fixed-top navbar-light py-0',
                    style={
                        'background-color': WHITE_ALPHA_8,
                        'border-bottom': '2px solid {0}'.format(BRAND)
                    },
                    children=[
                        html.A(href='#',
                               children=[
                                    html.H1(className='navbar-brand my-0',
                                            children=[
                                                html.Img(className='d-inline-block align-middle pb-1',
                                                         src=app.get_asset_url(
                                                             'RSE-community-logo.svg'),
                                                         width='40',
                                                         height='40'
                                                         ),
                                                html.Span(className='d-inline-block govuk-heading-s pl-2 mt-2 mb-0',
                                                          children='RSE Dashboard'
                                                          ),
                                            ]),
                               ]),
                        filters
                    ])
