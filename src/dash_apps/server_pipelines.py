import dash
from dash_apps.components.layout_pipelines import set_layout
from flask import Flask

server = Flask(__name__)

external_stylesheets = [
    '//stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
    '/static/css/govuk-frontend-3.4.0.min.css']

app = dash.Dash(__name__,
                server=server,
                external_stylesheets=external_stylesheets,
                requests_pathname_prefix='/dash/')

app.title = "RSE Pipelines Dashboard"
set_layout(app)
