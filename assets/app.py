# flake8: noqa
from flask import Flask, render_template
from flask_basicauth import BasicAuth
from time import sleep
import logging
import os
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'demo'
app.config['BASIC_AUTH_PASSWORD'] = 'mode'
basic_auth = BasicAuth(app)

def rf(name):
    content = ""
    with open(name, 'r') as buf:
        content = buf.read()
    return content


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/code.js")
def code():
    return render_template('code.js')


@app.route("/fetch")
def fetch():
    sleep(4)
    return render_template('fetch.json')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/secret')
@basic_auth.required
def secret_view():
    return render_template('index.html')

@app.route('/secret/sub')
@basic_auth.required
def secret_sub_view():
    return render_template('index.html')

if __name__ == "__main__":
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.logger.disabled = True
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'
    app.run()
