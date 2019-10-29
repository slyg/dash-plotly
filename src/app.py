import os.path
import time

import dash
import dash_html_components as html
import views.last_day_master_build_status as last_day_master_build_status

external_stylesheets = ['//fonts.googleapis.com/css?family=Roboto:300,300italic,700,700italic',
                        '//cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.css',
                        '//cdnjs.cloudflare.com/ajax/libs/milligram/1.3.0/milligram.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.H1(children='RSE Dash', style={
        'textAlign': 'center'
    }),

    html.Div(
        className='container',
        children=[

            html.Div(
                className='row',
                children=[
                    last_day_master_build_status.graph,
                    last_day_master_build_status.graph
                ])
        ])
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host="0.0.0.0")
