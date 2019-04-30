import json
import flask 
import flask_login 

from primo_website import controller
from primo_website import login_manager


mod = flask.Blueprint('account', __name__)

@mod.route("/accounts", methods=["GET"])
@flask_login.login_required
def _accounts():
    """
    Display the list of registered accounts.
    This page is only available for administrators
    """
    user = flask_login.current_user
    if user.category == "administrator":
        categories=["administrator", "physicist", "technologist", "nurse", "physician"]
        accounts = controller.accounts()
        return flask.render_template("accounts.html", accounts=accounts, categories=categories)
    return flask.redirect(flask.url_for('general.index'))
