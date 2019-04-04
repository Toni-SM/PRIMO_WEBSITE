from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

# database object
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.config)
    
    # register database
    db.init_app(app)

    # register blueprints
    from primo_website.views import general
    app.register_blueprint(general.mod)
    
    return app


def run():
    app = create_app()
    app.run(host=config.host, port=config.port)