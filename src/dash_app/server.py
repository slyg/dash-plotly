import dash
import dash_app.components.layout as layout
from flask import Flask

server = Flask(__name__)

external_stylesheets = [
    '//stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']

app = dash.Dash(__name__,
                server=server,
                external_stylesheets=external_stylesheets,
                requests_pathname_prefix='/dash/')

app.title = "RSE Dashboard"
layout.set_layout(app)
