#!/usr/bin/python3
""" Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def list_states(id=None):
    """ List availabale states when requesting /states or /states/<id> """

    res = storage.all(State).values()
    if id:
        for state in res:
            if state.id == id:
                return render_template('9-states.html', state=state,
                                       states=None)
        return render_template('9-states.html', state=None, states=None)
    return render_template('9-states.html', states=res, state=None)


@app.teardown_appcontext
def teardown_db(exception):
    """ Removes the current SQL Session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
