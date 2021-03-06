import sqlite3
import click
import logging
from flask import current_app
from flask import g
from flask.cli import with_appcontext
from flask.logging import default_handler

root = logging.getLogger()
root.addHandler(default_handler)


def get_db():
    # g is unique for each request
    # Can store data which can be accessed by multiple functions during
    # the request
    if 'db' not in g:
        g.db = sqlite3.connect(
            # Current app points to application handling request
            # current_app.config['DATABASE'] establishes connection
            # to file pointed at by the DATABASE key (it doesn't have
            # to exist yet)
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# NOTE: close_db gets an argument from flask when tearing down
#       The argument is exc_info()[1], i.e. the value of the latest
#       traceback
def close_db(exception=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

    if exception is not None:
        root.error(f'Caught exception with value: {exception}')


# NOTE: This is only called from the command line
def init_db():
    db = get_db()
    # Opens file relative to my_blog package
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# Click defines init-db as a CLI command
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)  # Teardown after response
    app.cli.add_command(init_db_command)  # Add flask CLI command

