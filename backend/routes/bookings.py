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

from flask import Blueprint, jsonify, request, send_file
import string

from components.decorators import disable_check, auth_required
from components.configuration import read_config
from components.objects.bookings import (
    get_bookings,
    get_available_seats_list,
    get_specific_booking_details,
)
from components.tools import is_integer
from components.db import sql_query
from components.swish_qr_generator import generate_swish_qr

from version import commit_hash, version

bookings_routes = Blueprint("bookings_routes", __name__)

BASEPATH = "/backend"
ILLEGAL_CHARACTERS = ["<", ">", ";"]
ALLOWED_CHARACTERS = list(string.printable) + ["å", "ä", "ö", "Å", "Ä", "Ö"]

NUM_TOTAL_SEATS = 48

config = read_config()

# bookings
@bookings_routes.route(f"{BASEPATH}/bookings", methods=["POST"])
@disable_check
@auth_required
def bookings():
    bookings_raw = get_bookings()
    bookings = []

    for booking in bookings_raw:
        bookings.append(
            {
                "id": booking[3],
                "name": booking[0],
                "school_class": booking[1],
                "status": booking[4],
                "date": str(booking[5]),
            }
        )

    return jsonify(
        {
            "status": True,
            "http_code": 200,
            "message": "request successful",
            "response": {"bookings": bookings},
        }
    )


@bookings_routes.route(f"{BASEPATH}/available_seat_list", methods=["POST"])
@disable_check
@auth_required
def available_seat_list():
    available_seat_list = get_available_seats_list()

    return jsonify(
        {
            "status": True,
            "http_code": 200,
            "message": "request successful",
            "response": {"available_seat_list": available_seat_list},
        }
    )


@bookings_routes.route(f"{BASEPATH}/book", methods=["POST"])
@disable_check
@auth_required
def book():
    if request.headers["content-type"] == "application/json":
        form_data = request.json

        # combine all input data and check for illegal characters and allowed characters
        all_input_data = ""
        for key, value in form_data.items():
            all_input_data = all_input_data + str(key)
            all_input_data = all_input_data + str(value)

        # validate data
        if any(x in all_input_data for x in ILLEGAL_CHARACTERS):
            return (
                jsonify(
                    {
                        "status": False,
                        "http_code": 400,
                        "message": "Någon av skickade variabler innehåller explicit otillåtna tecken.",
                        "response": {},
                    }
                ),
                400,
            )

        if any(x not in ALLOWED_CHARACTERS for x in all_input_data):
            return (
                jsonify(
                    {
                        "status": False,
                        "http_code": 400,
                        "message": "Någon av skickade variabler innehåller okända tecken. Endast alfabetet och Å, Ä och Ö tillåts.",
                        "response": {},
                    }
                ),
                400,
            )

        # check data
        for key, value in form_data.items():
            # check for extra/invalid keys
            if len(form_data) != 5:
                return (
                    jsonify(
                        {
                            "status": False,
                            "http_code": 400,
                            "message": "Saknar variabler.",
                            "response": {},
                        }
                    ),
                    400,
                )

            if (
                key != "token"
                and key != "name"
                and key != "class"
                and key != "email"
                and key != "seat"
            ):
                return (
                    jsonify(
                        {
                            "status": False,
                            "http_code": 400,
                            "message": "invalid keys sent",
                            "response": {},
                        }
                    ),
                    400,
                )

            # check for empty values
            if value == "":
                return (
                    jsonify(
                        {
                            "status": False,
                            "http_code": 400,
                            "message": f"{key} variabeln lämnades tom.",
                            "response": {},
                        }
                    ),
                    400,
                )

            # check if values are too short or too long
            if len(str(value)) < 3 or len(str(value)) > 50 and key != "token":
                if key != "seat":
                    return (
                        jsonify(
                            {
                                "status": False,
                                "http_code": 400,
                                "message": f"{key} variabeln är för kort eller för lång (mellan 3 och 50 tecken).",
                                "response": {},
                            }
                        ),
                        400,
                    )

            # check if class is too long
            if key == "class":
                if len(value) > 8:
                    return (
                        jsonify(
                            {
                                "status": False,
                                "http_code": 400,
                                "message": "Klass variabeln får max vara 8 karaktärer lång.",
                                "response": {},
                            }
                        ),
                        400,
                    )

            # validate email
            if key == "email":
                if not "@skola.botkyrka.se" in value:
                    return (
                        jsonify(
                            {
                                "status": False,
                                "http_code": 400,
                                "message": "Ogiltig e-postadress. Du måste använda skolmailadressen.",
                                "response": {},
                            }
                        ),
                        400,
                    )

            # check if seat is integer within range
            if key == "seat":
                if not is_integer(value):
                    return (
                        jsonify(
                            {
                                "status": False,
                                "http_code": 400,
                                "message": "seat must be integer",
                                "response": {},
                            }
                        ),
                        400,
                    )

                if int(value) < 1 or int(value) > NUM_TOTAL_SEATS:
                    return (
                        jsonify(
                            {
                                "status": False,
                                "http_code": 400,
                                "message": "value is outside allowed range",
                                "response": {},
                            }
                        ),
                        400,
                    )

        # check if seat is already booked or if this user has booked any other
        name = form_data["name"]
        school_class = form_data["class"].upper()
        email = form_data["email"]
        seat = form_data["seat"]

        already_used = False
        seat_taken = False
        for booking in get_bookings():
            if booking[2] == email:
                already_used = True
            if int(booking[3]) == int(seat):
                seat_taken = True

        if already_used or seat_taken:
            return (
                jsonify(
                    {
                        "status": False,
                        "http_code": 400,
                        "message": "Platsen du försöker boka är upptagen eller så har denna mailadress redan bokats av en annan plats.",
                        "response": {},
                    }
                ),
                400,
            )

        # if we've come this far, the input has then passed all validation

        # log ip
        if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
            remote_ip = request.environ["REMOTE_ADDR"]
        else:
            remote_ip = request.environ["HTTP_X_FORWARDED_FOR"]

        # create booking
        insert_booking = f"""INSERT INTO bookings (name, school_class, email, seat, status, date, ip) VALUES ('{name}', '{school_class}', '{email}', {seat}, 1, CURRENT_TIMESTAMP(), '{remote_ip}')"""

        # insert
        try:
            sql_query(insert_booking)
        except Exception:
            return (
                jsonify(
                    {
                        "status": False,
                        "http_code": 500,
                        "message": "Ett internt serverfel inträffade när bokningen skulle sparas. Kontakta Prytz via Discord om problemet kvarstår.",
                        "response": {},
                    }
                ),
                500,
            )

        # successful
        return (
            jsonify(
                {
                    "status": True,
                    "http_code": 201,
                    "message": "request successful",
                    "response": {},
                }
            ),
            201,
        )

    # invalid content-type
    return (
        jsonify(
            {
                "status": False,
                "http_code": 400,
                "message": "invalid content type",
                "response": {},
            }
        ),
        400,
    )


@bookings_routes.route(f"{BASEPATH}/swish/<id>", methods=["GET"])
@disable_check
def swish(id):
    # get specific id
    name = None
    school_class = None
    if id and is_integer(id):
        clicked_booking = get_specific_booking_details(id)

        if clicked_booking != None:
            name = clicked_booking[0]
            school_class = clicked_booking[1]
            seat = clicked_booking[3]

            generate_swish_qr(name, school_class, seat, 0)  # 0 means normal seat

            return send_file("static/temp_swish.png", mimetype="image/png")
        return (
            jsonify(
                {
                    "status": False,
                    "http_code": 400,
                    "message": "id does not exist",
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
                "message": "id is not defined or not integer",
                "response": {},
            }
        ),
        400,
    )
