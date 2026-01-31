from flask import Flask

app = Flask(__name__)

@app.route("/")
def blank():
    return "<p>nothing</p>"

@app.route("/<file>")
def page(file):
    return "<p>"+file+"</p>"

@app.route("/test/<sendUname>")
def sendUname(sendUname):
    return "<p>username: "+sendUname+"</p>"


if __name__ == "__main__":
    app.run(debug=True)