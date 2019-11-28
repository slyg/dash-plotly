from os import environ, path

from dash_app.server_pipelines import server as server_pipelines
from dash_app.server_security import server as server_security
from flask import (Flask, redirect, render_template, send_from_directory,
                   url_for)
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

root_server = Flask(__name__)


@root_server.route('/')
def index():
    return redirect('/dash')


@root_server.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html', title='Disclaimer')


@root_server.route('/favicon.ico')
def favicon():
    return send_from_directory(
        path.join(root_server.root_path, 'static/assets/images'), 'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )


root_app = DispatcherMiddleware(root_server, {
    '/dash': server_pipelines,
    '/security': server_security
})

if __name__ == '__main__':
    run_simple(hostname="0.0.0.0",
               port=int(environ['PORT']),
               application=root_app,
               use_reloader=False)
