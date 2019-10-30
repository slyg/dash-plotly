import os.path
import time

import dash
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
                    last_day_master_build_status.graph,
                    heatmap.graph
                ])
        ])
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host="0.0.0.0")
