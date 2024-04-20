#!/usr/bin/python3
""" Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """ Removes the current SQL Session """

    storage.close()


@app.route("/states_list", strict_slashes=False)
def list_states():
    """ List availabale states when requesting /states_list """

    res = storage.all(State).values()
    return render_template('7-states_list.html', states=res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
