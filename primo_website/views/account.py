import json
import flask 
import flask_login 

from primo_website import controller
from primo_website import login_manager


mod = flask.Blueprint('account', __name__)

@mod.route("/accounts", methods=["GET"])
def _accounts():
    """
    """
    categories=["administrator", "physicist", "technologist", "nurse", "physician"]
    accounts = controller.accounts()
    return flask.render_template("accounts.html", accounts=accounts, categories=categories)
