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

from flask import Blueprint, jsonify, request

from components.decorators import disable_check, auth_required
from components.objects.bookings import get_available_seats_list, get_bookings
from components.configuration import read_config
from components.session import (
    get_session,
    destroy_session,
    clear_old_sessions,
    new_session,
)

from version import commit_hash, version

basic_routes = Blueprint("basic_routes", __name__)

BASEPATH = "/backend"

config = read_config()

# application routes
@basic_routes.route(f"{BASEPATH}/info", methods=["GET"])
def info():
    return jsonify(
        {
            "status": True,
            "http_code": 200,
            "message": "request successful",
            "response": {
                "version": version,
                "commit_hash": commit_hash[0:6],
                "disabled": config["disabled"],
                "event_date": config["event_date"],
                "int_available_seats": int(len(get_available_seats_list())),
                "int_booked_seats": int(len(get_bookings())),
            },
        }
    )


@basic_routes.route(f"{BASEPATH}/auth", methods=["POST"])
@disable_check
def auth():
    # check for invalid length
    if len(request.json["password"]) < 3 or len(request.json["password"]) > 200:
        return (
            jsonify(
                {
                    "status": False,
                    "http_code": 400,
                    "message": "invalid password length (3 to 200 characters)",
                    "response": {},
                }
            ),
            400,
        )

    if request.json["password"] == config["lock_password"]:
        if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
            remote_ip = request.environ["REMOTE_ADDR"]
        else:
            remote_ip = request.environ["HTTP_X_FORWARDED_FOR"]

        clear_old_sessions()
        token = new_session(remote_ip, is_admin=False)

        if token != False:
            return jsonify(
                {
                    "status": True,
                    "http_code": 200,
                    "message": "request successful",
                    "response": {"session": token},
                }
            )
        else:
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

    return jsonify(
        {
            "status": False,
            "http_code": 401,
            "message": "Felaktigt lösenord.",
            "response": {},
        }
    )


@basic_routes.route(f"{BASEPATH}/validate_session", methods=["POST"])
@disable_check
@auth_required
def validate_session():
    # get user session
    session = get_session(request.json["token"])

    # if come this far, user would be authenticated
    return jsonify(
        {
            "status": True,
            "http_code": 200,
            "message": "valid session",
            "response": {"is_admin": session[3]},
        }
    )


@basic_routes.route(f"{BASEPATH}/logout", methods=["POST"])
@disable_check
@auth_required
def logout():
    # get user session
    session = get_session(request.json["token"])

    if destroy_session(request.json["token"]):
        return jsonify(
            {
                "status": True,
                "http_code": 200,
                "message": "session destroyed",
                "response": {},
            }
        )

    return (
        jsonify(
            {
                "status": False,
                "http_code": 500,
                "message": "Internal server error - unable to destroy session",
                "response": {},
            }
        ),
        500,
    )
