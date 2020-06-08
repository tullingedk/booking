###########################################################################
#                                                                         #
# tullingedk/booking                                                      #
# Copyright (C) 2018 - 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                         #
# Licensed under the terms of the GNU GPL-3.0 license, see LICENSE.       #
# https://github.com/tullingedk/booking                                   #
#                                                                         #
###########################################################################

from flask import Flask
from flask_cors import CORS

# imports
from version import version, commit_hash
from time import strftime
from os import environ, urandom

from base import base_req

from blueprints.auth import auth_blueprint
from blueprints.booking import booking_blueprint

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY") or urandom(24)

MYSQL_USER = environ.get("MYSQL_USER", "booking")
MYSQL_PASSWORD = environ.get("MYSQL_PASSWORD", "password")
MYSQL_HOST = environ.get("MYSQL_HOST", "127.0.0.1")
MYSQL_DATABASE = environ.get("MYSQL_DATABASE", "booking")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from models import db

db.init_app(app)

with app.app_context():
    db.create_all()


if not "DEVELOPMENT" in environ:
    CORS(app, resources={r"/*": {"origins": config["url"]}})
    print("Strict CORS-policy enabled")

if "DEVELOPMENT" in environ:
    CORS(app)
    print("Lazy CORS-policy enabled ('DEVELOPMENT' environment variable present)")


@app.errorhandler(400)
def error_400(e):
    return base_req(status=False, http_code=400, message=e.description)


@app.errorhandler(401)
def error_401(e):
    return base_req(status=False, http_code=401, message=e.description)


@app.errorhandler(403)
def error_403(e):
    return base_req(status=False, http_code=403, message=e.description)


@app.errorhandler(404)
def error_404(e):
    return base_req(status=False, http_code=404, message=e.description)


@app.errorhandler(405)
def error_405(e):
    return base_req(status=False, http_code=405, message=e.description)


@app.errorhandler(429)
def error_429(e):
    return base_req(status=False, http_code=429, message=e.description)


@app.errorhandler(500)
def error_500(e):
    return base_req(status=False, http_code=500, message=e.description)


# register blueprints
app.register_blueprint(auth_blueprint, url_prefix="/api/auth")
app.register_blueprint(booking_blueprint, url_prefix="/api/booking")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
