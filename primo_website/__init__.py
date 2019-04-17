from flask import Flask

import flask_login 
import flask_sqlalchemy

import config


# database object
db = flask_sqlalchemy.SQLAlchemy()

# login manager
login_manager = flask_login.LoginManager()


def create_app():
    """
    Create and return the Flask application
    
    Initialization of:
    - login manager
    - databases
    - blueprint mechanism
    """
    app = Flask(__name__)
    app.config.from_object(config.config)
    
    # init database
    db.init_app(app)
    
    # init login manager
    login_manager.init_app(app)
    login_manager.login_view = 'general.login'

    # register blueprints
    from primo_website.views import general
    app.register_blueprint(general.mod)
    
    return app


def run():
    app = create_app()
    app.run(host=config.host, port=config.port)