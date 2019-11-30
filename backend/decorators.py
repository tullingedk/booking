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
# Copyright (C) 2018 - 2019, Vilhelm Prytz <vilhelm@prytznet.se>                                             #
#                                                                                                            #
# This project is closed source. Allowed usage only covers the computer club on Tullinge gymnasium, Sweden.  #
# https://github.com/VilhelmPrytz/datorklubben-booking                                                       #
#                                                                                                            #
##############################################################################################################

# imports
import json
import os.path
from functools import wraps

from flask import jsonify, request
from session import *

# config
if os.path.exists("override.config.json"):
    with open("override.config.json", "r") as f:
        config = json.load(f)
else:
    with open("config.json", "r") as f:
        config = json.load(f)


def disable_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # check if system is in "disabled" mode
        if config["disabled"]:
            return (
                jsonify(
                    {
                        "status": False,
                        "http_code": 401,
                        "message": "Bokningssystemet är stängt.",
                        "response": {},
                    }
                ),
                401,
            )

        return f(*args, **kwargs)

    return decorated_function


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # check for authentication
        clear_old_sessions()
        if not validate_session(request.json["token"]):
            return (
                jsonify(
                    {
                        "status": False,
                        "http_code": 401,
                        "message": "Felaktig autentisering.",
                        "response": {},
                    }
                ),
                401,
            )
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # get remote ip
        if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
            remote_ip = request.environ["REMOTE_ADDR"]
        else:
            remote_ip = request.environ["HTTP_X_FORWARDED_FOR"]

        # check for authentication
        clear_old_sessions()
        if not validate_session(request.json["token"]):
            return (
                jsonify(
                    {
                        "status": False,
                        "http_code": 401,
                        "message": "Felaktig autentisering.",
                        "response": {},
                    }
                ),
                401,
            )

        # check if ip has changed
        session = get_session(request.json["token"])
        if session[2] != remote_ip:
            return (
                jsonify(
                    {
                        "status": False,
                        "http_code": 401,
                        "message": "user ip has changed",
                        "response": {},
                    }
                ),
                401,
            )

        # check if admin
        if session[3] != 1:
            return (
                jsonify(
                    {
                        "status": False,
                        "http_code": 401,
                        "message": "user is not admin",
                        "response": {},
                    }
                ),
                401,
            )

        return f(*args, **kwargs)

    return decorated_function
