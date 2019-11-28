import dash
import dash_app.components.layout as layout
from flask import Flask

server = Flask(__name__)

external_stylesheets = [
    '//stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
    '/static/css/govuk-frontend-3.4.0.min.css']

app = dash.Dash(__name__,
                server=server,
                external_stylesheets=external_stylesheets,
                requests_pathname_prefix='/security/')

app.title = "RSE Security Dashboard"
layout.set_security_layout(app)
