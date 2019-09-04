# flake8: noqa
from flask import Flask, render_template
from time import sleep
app = Flask(__name__)


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
