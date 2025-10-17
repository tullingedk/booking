###########################################################################
#                                                                         #
# tullingedk/booking                                                      #
# Copyright (C) 2018 - 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                         #
# Licensed under the terms of the GNU GPL-3.0 license, see LICENSE.       #
# https://github.com/tullingedk/booking                                   #
#                                                                         #
###########################################################################

from flask import Flask, abort, request
from flask_cors import CORS

# imports
from os import environ
from datetime import timedelta

from base import base_req
from models import db

from blueprints.auth import auth_blueprint
from blueprints.booking import booking_blueprint
from blueprints.admin import admin_blueprint

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY")

# Session Security Configuration
app.config['SESSION_COOKIE_SECURE'] = environ.get("DEVELOPMENT") is None  # True in production
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Primary CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)  # 2-hour session timeout
app.config['SESSION_REFRESH_EACH_REQUEST'] = True  # Refresh timeout on activity

MYSQL_USER = environ.get("MYSQL_USER", "booking")
MYSQL_PASSWORD = environ.get("MYSQL_PASSWORD", "password")
MYSQL_HOST = environ.get("MYSQL_HOST", "127.0.0.1")
MYSQL_DATABASE = environ.get("MYSQL_DATABASE", "booking")
BACKEND_URL = environ.get("BACKEND_URL", "http://localhost:5000")
DISABLED = environ.get("DISABLED", None)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

if "DEVELOPMENT" not in environ:
    CORS(app, resources={r"/*": {"origins": BACKEND_URL}})
    print("Strict CORS-policy enabled")

if "DEVELOPMENT" in environ:
    CORS(app, supports_credentials=True)
    print("Lazy CORS-policy enabled ('DEVELOPMENT' environment variable present)")


@app.errorhandler(400)
def error_400(e):
    return base_req(status=False, http_code=400, message=e.description)


@app.errorhandler(401)
def error_401(e):
    return base_req(
        status=False,
        http_code=401,
        message=e.description["description"]
        if type(e.description) is dict
        else e.description,
        response=e.description["response"] if type(e.description) is dict else {},
    )


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


@app.errorhandler(501)
def error_501(e):
    return base_req(status=False, http_code=501, message=e.description)


@app.errorhandler(503)
def error_503(e):
    return base_req(status=False, http_code=503, message=e.description)


# CSRF Protection via Origin/Referer validation (works without tokens!)
@app.before_request
def csrf_protection():
    # Skip CSRF check for safe methods and OAuth callback
    if request.method in ['GET', 'HEAD', 'OPTIONS']:
        return
    
    # Skip for OAuth callback endpoint (Google redirects here)
    if request.endpoint and 'auth.callback' in request.endpoint:
        return
    
    # Get origin and referer headers
    origin = request.headers.get('Origin')
    referer = request.headers.get('Referer')
    
    # Allow requests from the same origin
    allowed_origins = [BACKEND_URL, FRONTEND_URL]
    
    # In development, be more permissive
    if "DEVELOPMENT" in environ:
        if origin or referer:  # Just check that headers exist in dev
            return
    else:
        # Production: strict origin validation
        if origin and origin in allowed_origins:
            return
        if referer:
            for allowed in allowed_origins:
                if referer.startswith(allowed):
                    return
        
        # No valid origin/referer - potential CSRF attack
        abort(403, "CSRF validation failed. Invalid origin.")

# disabled check
@app.before_request
def disabled_check():
    if DISABLED:
        abort(503, DISABLED)


# register blueprints
app.register_blueprint(auth_blueprint, url_prefix="/api/auth")
app.register_blueprint(booking_blueprint, url_prefix="/api/booking")
app.register_blueprint(admin_blueprint, url_prefix="/api/admin")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
