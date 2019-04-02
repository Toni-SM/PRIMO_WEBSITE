from flask import Flask

import config

app = Flask(__name__)
app.config.from_object(config.config)

# register blueprints
from primo_website.views import general

app.register_blueprint(general.mod)


def run():
    app.run(host=config.host, port=config.port)