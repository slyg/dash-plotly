import os.path
import time

import dash
import views.layout as layout

external_stylesheets = [
    '//stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "RSE Dashboard"
layout.set_layout(app)

if __name__ == '__main__':
    app.run_server(debug=False, port=8050, host="0.0.0.0")
