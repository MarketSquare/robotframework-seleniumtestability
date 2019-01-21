from flask import Flask, render_template, request
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


@app.route("/api.js")
def api():
    return rf('../src/SeleniumTestability/testability/api.js')


@app.route("/bindings.js")
def bindings():
    return rf('../src/SeleniumTestability/testability/bindings.js')


@app.route("/code.js")
def code():
    return render_template('code.js')


@app.route("/fetch")
def fetch():
    sleep(4)
    return render_template('fetch.json')


@app.route('/')
def index():
    inj_bindings = '<script type="text/javascript" src="bindings.js"></script>'
    inj_api = '<script type="text/javascript" src="api.js"></script>'
    inject = request.args.get('inject', default=1, type=int) == 1
    if inject:
        inj_api = ''
        inj_bindings = ''
    return render_template('index.html', apitag=inj_api, bindingstag=inj_bindings)
