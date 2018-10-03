from flask import Flask, render_template, request
from time import sleep
app = Flask(__name__)

def rf(name):
    content = ""
    with open(name,'r') as buf:
        content = buf.read()
    return content 

@app.route("/api.js")
def api():
    return  rf('www/api.js')

@app.route("/bindings.js")
def bindings():
    return  rf('www/bindings.js')

@app.route("/code.js")
def code():
    return  rf('www/code.js')

@app.route("/fetch")
def fetch():
    sleep(4)
    return render_template('fetch.json')

@app.route('/')
def index():
    inj_api = '<script type="text/javascript" src="api.js"></script>'
    inj_bindings = '<script type="text/javascript" src="bindings.js"></script>'
    inject = request.args.get('inject', default = 1, type = int) == 1
    if not inject:
        inj_api = ''
        inj_bindings = ''
    return render_template('index.html', apitag=inj_api, bindingstag=
            inj_bindings)
