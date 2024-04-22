#!/usr/bin/python3
""" Flask web app """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def dispose(exception):
    """ Remove current session """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states():
    """ Display list of all the states """
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
