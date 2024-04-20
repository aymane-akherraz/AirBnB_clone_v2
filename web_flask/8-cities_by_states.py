#!/usr/bin/python3
""" Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_state():
    """
        List availabale states with their cities when requesting
        /cities_by_states
    """

    res = storage.all(State)
    return render_template('8-cities_by_states.html', states=res.values())


@app.teardown_appcontext
def teardown_db(exception):
    """ Removes the current SQL Session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
