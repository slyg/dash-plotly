import os.path
import time

import dash
import flask
import views.layout as layout

server = flask.Flask(__name__)


@server.route('/')
def index():
    return 'Hello, go to dash/'


external_stylesheets = [
    '//stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']

dash_app = dash.Dash(__name__,
                     server=server,
                     external_stylesheets=external_stylesheets,
                     routes_pathname_prefix='/dash/')

dash_app.title = "RSE Dashboard"
layout.set_layout(dash_app)

if __name__ == '__main__':
    dash_app.run_server(debug=False, port=8050, host="0.0.0.0")
