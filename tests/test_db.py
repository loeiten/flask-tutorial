import sqlite3

import pytest
from my_blog.db import get_db


def test_get_close_db(app):
    # get_db should return the same connection each time it’s called
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    # After the context, the connection should be closed
    assert 'closed' in str(e)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('my_blog.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    # The init-db command should call the init_db function and output
    # a message.
    assert 'Initialized' in result.output
    assert Recorder.called
