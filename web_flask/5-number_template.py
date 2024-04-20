#!/usr/bin/python3
""" Flask web application """
from flask import Flask, abort, render_template
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


@app.route("/python/", defaults={'text': "is cool"})
@app.route("/python/<text>", strict_slashes=False)
def Py_text(text):
    """
        Displays Python followed by the value of the text variable
        if text is not given, it displays 'Python is cool'
    """

    return "Python {}".format(escape(text.replace("_", " ")))


@app.route("/number/<n>", strict_slashes=False)
def nb(n):
    """ Displays 'n is a number' only if n is an integer """

    try:
        n = int(n)
        return "{} is a number".format(n)
    except ValueError:
        abort(404)


@app.route("/number_template/<n>", strict_slashes=False)
def nb_tmp(n):
    """ Displays a HTML page only if n is an integer """
    try:
        n = int(n)
        return render_template('5-number.html', nb=n)
    except ValueError:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
