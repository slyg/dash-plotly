import dash_core_components as dcc
import dash_html_components as html
from style.theme import BRAND, WHITE_ALPHA_8

project_default_value = 'all'
project_opts = [

    {'label': 'All',
     'value': 'all'},

    {'label': 'Bulk Scanning',
     'value': '_BSP'},

    {'label': 'CCD',
     'value': '_CDM'},

    {'label': 'CET',
     'value': '_CET'},

    {'label': 'CMC',
     'value': '_CMC'},

    {'label': 'CNP',
     'value': '_CNP'},

    {'label': 'CTSC',
     'value': '_CTSC'},

    {'label': 'DevOps',
     'value': '_DevOps'},

    {'label': 'DIV',
     'value': '_DIV'},

    {'label': 'Ethos replacement',
     'value': '_ETHOS'},

    {'label': 'Fees and Pay',
     'value': '_FeePay'},

    {'label': 'Financial Remedy',
     'value': '_FinRem'},

    {'label': 'FPL',
     'value': '_FPL'},

    {'label': 'IAC',
     'value': '_IAC'},

    {'label': 'IDAM',
     'value': '_IDAM'},

    {'label': 'Management Information',
     'value': '_MI'},

    {'label': 'Platform',
     'value': '_Platform'},

    {'label': 'Probate',
     'value': '_Probate'},

    {'label': 'Reference Data',
     'value': '_RD'},

    {'label': 'RPA',
     'value': '_RPA'},

    {'label': 'SL',
     'value': '_SL'},

    {'label': 'SCSS',
     'value': '_SSCS'},
]

pipeline_type_default_value = 'all'
pipeline_type_opts = [

    {'label': 'All',
     'value': 'all'},

    {'label': 'Nightly',
     'value': 'nightly'},

    {'label': 'Non-nightly',
     'value': 'non-nightly'},
]


def getHeader(app):
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
                    ])


def getNavigation(app):
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
                        html.Div(className='form-inline my-2 my-lg-0 govuk-body-s',
                                 children=[
                                     html.Form(className="pl-5",
                                               children=[
                                                   html.Label(className='d-inline-block pr-2 py-2 text-dark small',
                                                              htmlFor='project',
                                                              children='Project'
                                                              ),
                                                   html.Div(className="d-inline-block align-middle",
                                                            children=[
                                                                dcc.Dropdown(
                                                                      id="project",
                                                                      className="small nav-form-width",
                                                                      clearable=False,
                                                                      options=project_opts,
                                                                      value=project_default_value),
                                                            ])
                                               ]),
                                     html.Form(className="pl-5",
                                               children=[
                                                   html.Label(className='d-inline-block pr-2 py-2 text-dark small',
                                                              htmlFor='pipeline-type',
                                                              children='Nightly / Non-nightly'
                                                              ),
                                                   html.Div(className="d-inline-block align-middle",
                                                            children=[
                                                                dcc.Dropdown(id="pipeline-type",
                                                                             clearable=False,
                                                                             className="small nav-form-width",
                                                                             options=pipeline_type_opts,
                                                                             value=pipeline_type_default_value),
                                                            ])
                                               ])


                                 ]),
                    ])
