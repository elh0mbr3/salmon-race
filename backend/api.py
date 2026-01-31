from flask import Flask

app = Flask(__name__)

@app.route("/")
def blank():
    return "<p>nothing</p>"

@app.route("/<file>")
def page(file):
    return "<p>"+file+"</p>"

@app.route("/sendUname")
def sendUname():
    #create Player object

def 