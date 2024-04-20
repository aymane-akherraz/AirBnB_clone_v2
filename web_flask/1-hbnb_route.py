#!/usr/bin/python3
""" Flask web application """
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_world():
    """ Displays Hello HBNB! when requesting /"""

    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def HBNB():
    """ Displays HBNB when requesting /hbnb"""

    return "HBNB"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
