#!/usr/bin/python3
""" Flask web application """
from flask import Flask
from markupsafe import escape
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_world():
    """ Displays Hello HBNB! when requesting /"""

    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def HBNB():
    """ Displays HBNB when requesting /hbnb"""

    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def C_text(text):
    """ Displays C followed by the value of the text variable """

    return "C {}".format(escape(text.replace("_", " ")))


@app.route("/python/")
@app.route("/python/<text>", strict_slashes=False)
def Py_text(text="is cool"):
    """ Displays Python followed by the value of the text variable """

    return "Python {}".format(escape(text.replace("_", " ")))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
