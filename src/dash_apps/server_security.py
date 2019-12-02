import dash
from dash_apps.components.layout_security import set_layout
from dash_apps.lib.external_deps import external_scripts, external_stylesheets
from flask import Flask

server = Flask(__name__)

app = dash.Dash(__name__,
                server=server,
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts,
                requests_pathname_prefix='/security/')

app.title = "RSE Security Dashboard"
set_layout(app)
