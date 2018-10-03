from flask import Flask, render_template
from time import sleep
app = Flask(__name__)

inj_api = None
inj_bindings  = None

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
    sleep(10)
    return render_template('index.html', api_code=inj_api, bindings_code =
            inj_bindings)

@app.route('/')
def index():
    print(inj_api)
    return render_template('index.html', api_code=inj_api, bindings_code =
            inj_bindings)
