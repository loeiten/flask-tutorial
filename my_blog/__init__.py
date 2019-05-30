from flask import Flask
from pathlib import Path
from my_blog.db import init_app
from my_blog import auth
from my_blog import blog


# NOTE: create_app is a function which flask searches for when
#       running the CLI
def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # NOTE: Originally referred to app.instance_path
    instance_path = Path(__file__).absolute().parents[1].\
        joinpath('instance')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=instance_path.joinpath('my_blog.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    instance_path.mkdir(parents=True, exist_ok=True)

    # NOTE: As create_app is something the flask CLI is searching
    #       for, we register the init_app command line here
    init_app(app)

    # Register the auth blueprint
    app.register_blueprint(auth.bp)
    # Register the blog blueprint
    app.register_blueprint(blog.bp)
    # Associates the endpoint name 'index' with the / url so that
    # url_for('index') or url_for('blog.index') will both work
    app.add_url_rule('/', endpoint='index')

    return app


if __name__ == '__main__':
    app_ = create_app()
    app_.run(debug=True, host='0.0.0.0', port='5000')