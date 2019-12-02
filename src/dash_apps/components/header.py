import dash_core_components as dcc
import dash_html_components as html
from style.theme import BRAND, WHITE_ALPHA_8


def getHeader(app, filters=None):
    return html.Nav(className='navbar fixed-top navbar-light navbar-expand-lg py-0',
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
                        html.Button(className='navbar-toggler',
                                    type='button',
                                    **{
                                        'data-toggle': 'collapse',
                                        'data-target': '#navbarNav',
                                        'aria-controls': 'navbarNav',
                                        'aria-expanded': 'false',
                                        'aria-label': 'Toggle navigation'
                                    },
                                    children=[
                                        html.Span(
                                            className='navbar-toggler-icon')
                                    ]),
                        html.Div(className='collapse navbar-collapse',
                                 id='navbarNav',
                                 children=[
                                     html.Ul(className='navbar-nav mr-auto',
                                             children=[
                                                 html.Li(className='nav-item',
                                                         children=[
                                                             html.A(className='nav-link govuk-link',
                                                                    href='/pipelines',
                                                                    children='Pipelines')
                                                         ]),
                                                 html.Li(className='nav-item',
                                                         children=[
                                                             html.A(className='nav-link govuk-link',
                                                                    href='/security',
                                                                    children='Security')
                                                         ]),
                                             ]),
                                     filters,
                                 ]),
                    ])
