import dash_core_components as dcc
import dash_html_components as html
from style.theme import BRAND, LIGHT_GREY, WHITE


def layout(app, header, body):
    return html.Div(
        id="top",
        children=[
            html.Div(
                className='container-fluid',
                style={
                    'background-color': LIGHT_GREY,
                },
                children=[
                    html.Div(
                        className='row my-3',
                        children=[
                            html.Div(className='col col-12',
                                     children=header),
                        ]),
                    html.Div(
                        className='row mt-5',
                        children=body),
                    html.Div(
                        className='row mt-0 govuk-footer pt-0 pb-0',
                        style={
                            'background-color': WHITE,
                        },
                        children=[
                            html.Div(className='col col-12 my-3 govuk-body-s',
                                     children=[
                                         html.Ul(className='govuk-footer__inline-list mb-0',
                                                 children=[
                                                     html.Li(className='govuk-footer__inline-list-item',
                                                             children=[
                                                                 html.A(href='/disclaimer',
                                                                        className='govuk-footer__link',
                                                                        children='Disclaimer'),
                                                             ]),
                                                     html.Li(className='govuk-footer__inline-list-item',
                                                             children=[
                                                                 html.A(href='https://github.com/hmcts/RSE-dashboard',
                                                                        className='govuk-footer__link',
                                                                        children='Source'),
                                                             ])

                                                 ]),
                                     ]),
                        ]),
                ])

        ])
