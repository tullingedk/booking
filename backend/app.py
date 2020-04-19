#!/usr/bin/env python3

##############################################################################################################
#   _____        _             _    _       _     _                  ____              _    _                #
#  |  __ \      | |           | |  | |     | |   | |                |  _ \            | |  (_)               #
#  | |  | | __ _| |_ ___  _ __| | _| |_   _| |__ | |__   ___ _ __   | |_) | ___   ___ | | ___ _ __   __ _    #
#  | |  | |/ _` | __/ _ \| '__| |/ / | | | | '_ \| '_ \ / _ \ '_ \  |  _ < / _ \ / _ \| |/ / | '_ \ / _` |   #
#  | |__| | (_| | || (_) | |  |   <| | |_| | |_) | |_) |  __/ | | | | |_) | (_) | (_) |   <| | | | | (_| |   #
#  |_____/ \__,_|\__\___/|_|  |_|\_\_|\__,_|_.__/|_.__/ \___|_| |_| |____/ \___/ \___/|_|\_\_|_| |_|\__, |   #
#                                                                                                    __/ |   #
#                                                                                                   |___/    #
#                                                                                                            #
# Copyright (C) 2018 - 2020, Vilhelm Prytz <vilhelm@prytznet.se>                                             #
#                                                                                                            #
# This project is closed source. Allowed usage only covers the computer club on Tullinge gymnasium, Sweden.  #
# https://github.com/VilhelmPrytz/datorklubben-booking                                                       #
#                                                                                                            #
##############################################################################################################

# imports
from flask import Flask, jsonify
from flask_cors import CORS
from os import environ

from components.configuration import read_config
from components.tools import get_client_ip

# blueprints
from routes.basic import basic_routes
from routes.bookings import bookings_routes
from routes.bc_bookings import bc_bookings_routes
from routes.admin import admin_routes

# limiter from core
from components.core import limiter

# configuration
config = read_config()

# validate some configuration values
if (
    len(config["lock_password"]) < 3
    or len(config["lock_password"]) > 200
    or len(config["admin_password"]) < 3
    or len(config["admin_password"]) > 200
):
    raise Exception("passwords should be 3 to 200 characters long")

# flask application
app = Flask(__name__)

if not "DEVELOPMENT" in environ:
    CORS(app, resources={r"/*": {"origins": config["url"]}})
    print("Strict CORS-policy enabled")

if "DEVELOPMENT" in environ:
    CORS(app)
    print("Lazy CORS-policy enabled ('DEVELOPMENT' environment variable present)")


# flaks app config
app.config[
    "RATELIMIT_STORAGE_URL"
] = f"redis://{config['redis']['host']}:{config['redis']['port']}"

limiter.init_app(app)

# error routes
@app.errorhandler(400)
def error_400(e):
    return (
        jsonify(
            {
                "status": False,
                "http_code": 400,
                "message": "Felaktig begäran.",
                "response": {},
            }
        ),
        400,
    )


@app.errorhandler(401)
def error_401(e):
    return (
        jsonify(
            {
                "status": False,
                "http_code": 401,
                "message": "Åtkomst nekas.",
                "response": {},
            }
        ),
        401,
    )


@app.errorhandler(404)
def error_404(e):
    return (
        jsonify(
            {
                "status": False,
                "http_code": 404,
                "message": "Resursen du söker hittades inte.",
                "response": {},
            }
        ),
        404,
    )


@app.errorhandler(405)
def error_405(e):
    return (
        jsonify(
            {
                "status": False,
                "http_code": 405,
                "message": "Felaktig begäran, ej tillåten metod.",
                "response": {},
            }
        ),
        405,
    )


@app.errorhandler(429)
def error_429(e):
    return (
        jsonify(
            {
                "status": False,
                "http_code": 429,
                "message": "too many requests, you are being rate limited",
                "response": {},
            }
        ),
        429,
    )


@app.errorhandler(500)
def error_500(e):
    return (
        jsonify(
            {
                "status": False,
                "http_code": 500,
                "message": "Internt serverfel inträffade.",
                "response": {},
            }
        ),
        500,
    )


# register blueprints
app.register_blueprint(basic_routes)
app.register_blueprint(bookings_routes)
app.register_blueprint(bc_bookings_routes)
app.register_blueprint(admin_routes)

# run application
if __name__ == "__main__":
    app.run(host="0.0.0.0")
