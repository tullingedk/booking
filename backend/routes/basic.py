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

from flask import Blueprint, jsonify, request, abort

from components.decorators import disable_check, auth_required
from components.objects.bookings import get_available_seats_list, get_bookings
from components.objects.bc_bookings import bc_get_available_seats_list, get_bc_bookings
from components.configuration import read_config
from components.session import (
    get_session,
    destroy_session,
    clear_old_sessions,
    new_session,
)
from components.core import limiter
from components.db import dict_sql_query
from components.google import google_login

from version import commit_hash, version

basic_routes = Blueprint("basic_routes", __name__)

BASEPATH = "/backend"

config = read_config()

# application routes
@basic_routes.route(f"{BASEPATH}/info", methods=["GET"])
@limiter.limit("200 per hour")
@limiter.limit("5 per second")
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
                "bc_int_available_seats": int(len(bc_get_available_seats_list())),
                "bc_int_booked_seats": int(len(get_bc_bookings())),
                "google_signin": config["google_signin"],
            },
        }
    )


@basic_routes.route(f"{BASEPATH}/google_callback", methods=["POST"])
@limiter.limit("50 per hour")
@disable_check
def google_callback():
    if not config["google_signin"]:
        abort(400)

    if not request.get_json("idtoken"):
        return (
            jsonify(
                {
                    "status": False,
                    "http_code": 400,
                    "message": "missing form data",
                    "response": {},
                }
            ),
            400,
        )

    # verify using separate module
    google = google_login(request.json["idtoken"], config["gsuite_domain_name"])

    if not google["status"]:
        return google["resp"]

    data = google["resp"]["data"]

    # perform some validation against database
    if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
        remote_ip = request.environ["REMOTE_ADDR"]
    else:
        remote_ip = request.environ["HTTP_X_FORWARDED_FOR"]

    # lookup user
    user = dict_sql_query(
        f'SELECT * FROM users WHERE email="{data["email"]}"', fetchone=True
    )

    if not user and not request.json["create"]:
        return (
            jsonify(
                {
                    "status": False,
                    "http_code": 401,
                    "message": "Användaren är inte konfigurerad.",
                    "response": {"configure_user": True,},
                }
            ),
            401,
        )

    # create user
    if not user and request.json["create"]:
        if request.json["password"] != config["lock_password"]:
            return (
                (
                    jsonify(
                        {
                            "status": False,
                            "http_code": 401,
                            "message": "Fel lösenord",
                            "response": {},
                        }
                    )
                ),
                401,
            )

        if not request.get_json("class"):
            abort(400)

        _class = request.json["class"]

        if len(_class) < 3 or len(_class) > 6:
            abort(400)

        dict_sql_query(
            f'INSERT INTO users VALUES ("{data["email"]}", "{request.json["class"].upper()}")',
            fetchone=True,
        )
        user = dict_sql_query(
            f'SELECT * FROM users WHERE email="{data["email"]}"', fetchone=True
        )

    school_class = user["school_class"]

    clear_old_sessions()
    token = new_session(
        remote_ip, data["name"], data["email"], school_class, is_admin=False
    )

    if token is not False:
        return jsonify(
            {
                "status": True,
                "http_code": 200,
                "message": "request successful",
                "response": {
                    "configure_user": False,
                    "session": token,
                    "email": data["email"],
                    "name": data["name"],
                    "picture_url": data["picture"],
                    "school_class": school_class,
                },
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


@basic_routes.route(f"{BASEPATH}/auth", methods=["POST"])
@limiter.limit("50 per hour")
@disable_check
def auth():
    if config["google_signin"]:
        abort(400)

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
        token = new_session(remote_ip, None, None, None, is_admin=False)

        if token is not False:
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
@limiter.limit("500 per hour")
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
            "response": {"is_admin": session[6]},
        }
    )


@basic_routes.route(f"{BASEPATH}/logout", methods=["POST"])
@limiter.limit("500 per hour")
@disable_check
@auth_required
def logout():
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
