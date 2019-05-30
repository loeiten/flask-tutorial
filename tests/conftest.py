import tempfile
import pytest
from pathlib import Path
from my_blog import create_app
from my_blog.db import get_db
from my_blog.db import init_db


test_dir = Path(__file__).absolute().parent
with test_dir.joinpath('data.sql').open('rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    # tempfile.mkstemp() creates and opens a temporary file, returning
    # the file object and the path to it
    _, db_path = tempfile.mkstemp()

    app = create_app({
        # TESTING tells Flask that the app is in test mode
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    db_path = Path(db_path)
    db_path.unlink()


@pytest.fixture
def client(app):
    # Tests will use the client to make requests to the application
    # without running the server
    return app.test_client()


@pytest.fixture
def runner(app):
    # Creates a runner that can call the Click commands registered
    # with the application
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        # NOTE: hashed password are easy to forward compute,
        #       hopefully hard to backwards compute
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
