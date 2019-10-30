import os.path
import time

import dash
import dash_core_components as dcc
import dash_html_components as html
import views.heatmap as heatmap
import views.last_day_master_build_status as last_day_master_build_status

external_stylesheets = [
    '//stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.H1(children='RSE Dashboard', style={
        'textAlign': 'center',
        'fontSize': 15
    }),

    html.Div(
        className='container-fluid',
        children=[
            html.Div(
                className='row',
                children=[
                    dcc.Graph(
                        className='col col-md-6',
                        figure=last_day_master_build_status.figure
                    ), dcc.Graph(
                        className='col col-md-6',
                        figure=heatmap.figure
                    )
                ])
        ])
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host="0.0.0.0")
