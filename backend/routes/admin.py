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

from components.decorators import disable_check, admin_required
from components.objects.bookings import get_specific_booking_details
from components.objects.bc_bookings import get_specific_bc_booking_details
from components.configuration import read_config
from components.session import clear_old_sessions, new_session
from components.db import sql_query
from components.tools import is_integer, get_client_ip
from components.core import limiter

admin_routes = Blueprint("admin_routes", __name__)

BASEPATH = "/backend"

config = read_config()


@admin_routes.route(f"{BASEPATH}/admin/auth", methods=["POST"])
@limiter.limit("5 per hour")
@disable_check
def admin_auth():
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

    if request.json["password"] == config["admin_password"]:
        remote_ip = get_client_ip()
        clear_old_sessions()
        token = new_session(remote_ip, is_admin=True)

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


@admin_routes.route(f"{BASEPATH}/admin/paid/<id>", methods=["POST"])
@limiter.limit("200 per hour")
@limiter.limit("5 per second")
@disable_check
@admin_required
def admin_paid(id):
    if is_integer(id):
        booking = get_specific_booking_details(id)

        if booking != None:
            try:
                sql_query(f"UPDATE bookings SET status=0 WHERE seat={id}")
            except Exception:
                return (
                    jsonify(
                        {
                            "status": False,
                            "http_code": 500,
                            "message": "Ett internt serverfel inträffade.",
                            "response": {},
                        }
                    ),
                    500,
                )

            return jsonify(
                {
                    "status": True,
                    "http_code": 200,
                    "message": "request successful",
                    "response": {},
                }
            )
        return (
            jsonify(
                {
                    "status": False,
                    "http_code": 400,
                    "message": "Denna bokning existerar inte.",
                    "response": {},
                }
            ),
            400,
        )

    return (
        jsonify(
            {
                "status": False,
                "http_code": 400,
                "message": "id must be integer",
                "response": {},
            }
        ),
        400,
    )


@admin_routes.route(f"{BASEPATH}/admin/unpaid/<id>", methods=["POST"])
@limiter.limit("200 per hour")
@limiter.limit("5 per second")
@disable_check
@admin_required
def admin_unpaid(id):
    if is_integer(id):
        booking = get_specific_booking_details(id)

        if booking != None:
            try:
                sql_query(f"UPDATE bookings SET status=1 WHERE seat={id}")
            except Exception:
                return (
                    jsonify(
                        {
                            "status": False,
                            "http_code": 500,
                            "message": "Ett internt serverfel inträffade.",
                            "response": {},
                        }
                    ),
                    500,
                )

            return jsonify(
                {
                    "status": True,
                    "http_code": 200,
                    "message": "request successful",
                    "response": {},
                }
            )
        return (
            jsonify(
                {
                    "status": False,
                    "http_code": 400,
                    "message": "Denna bokning existerar inte.",
                    "response": {},
                }
            ),
            400,
        )

    return (
        jsonify(
            {
                "status": False,
                "http_code": 400,
                "message": "id must be integer",
                "response": {},
            }
        ),
        400,
    )


@admin_routes.route(f"{BASEPATH}/admin/bc/paid/<id>", methods=["POST"])
@limiter.limit("200 per hour")
@limiter.limit("5 per second")
@disable_check
@admin_required
def admin_bc_paid(id):
    if is_integer(id):
        booking = get_specific_bc_booking_details(id)

        if booking != None:
            try:
                sql_query(f"UPDATE bc_bookings SET status=0 WHERE seat={id}")
            except Exception:
                return (
                    jsonify(
                        {
                            "status": False,
                            "http_code": 500,
                            "message": "Ett internt serverfel inträffade.",
                            "response": {},
                        }
                    ),
                    500,
                )

            return jsonify(
                {
                    "status": True,
                    "http_code": 200,
                    "message": "request successful",
                    "response": {},
                }
            )
        return (
            jsonify(
                {
                    "status": False,
                    "http_code": 400,
                    "message": "Denna bokning existerar inte.",
                    "response": {},
                }
            ),
            400,
        )

    return (
        jsonify(
            {
                "status": False,
                "http_code": 400,
                "message": "id must be integer",
                "response": {},
            }
        ),
        400,
    )


@admin_routes.route(f"{BASEPATH}/admin/bc/unpaid/<id>", methods=["POST"])
@limiter.limit("200 per hour")
@limiter.limit("5 per second")
@disable_check
@admin_required
def admin_bc_unpaid(id):
    if is_integer(id):
        booking = get_specific_bc_booking_details(id)

        if booking != None:
            try:
                sql_query(f"UPDATE bc_bookings SET status=1 WHERE seat={id}")
            except Exception:
                return (
                    jsonify(
                        {
                            "status": False,
                            "http_code": 500,
                            "message": "Ett internt serverfel inträffade.",
                            "response": {},
                        }
                    ),
                    500,
                )

            return jsonify(
                {
                    "status": True,
                    "http_code": 200,
                    "message": "request successful",
                    "response": {},
                }
            )
        return (
            jsonify(
                {
                    "status": False,
                    "http_code": 400,
                    "message": "Denna bokning existerar inte.",
                    "response": {},
                }
            ),
            400,
        )

    return (
        jsonify(
            {
                "status": False,
                "http_code": 400,
                "message": "id must be integer",
                "response": {},
            }
        ),
        400,
    )
