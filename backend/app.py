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
from flask import Flask, jsonify, request
from flask_cors import CORS
import os.path

# modules
from tools import *
from db import *
from decorators import *
from session import *
from version import version
from swish_qr_generator import generate_swish_qr

# variables
BASEPATH = "/backend"

# configuration
if os.path.exists("override.config.json"):
    with open("override.config.json", 'r') as f:
        config = json.load(f)
else:
    with open("config.json", 'r') as f:
        config = json.load(f)

# flask application
app = Flask(__name__)
CORS(app)

# functions
def get_bookings():
    """Returns list of all bookings"""

    if config["development"]:
        return dev_bookings
    else:
        return sql_query("SELECT * FROM bookings")

def get_available_seats_list():
    """Returns list of available booking seats"""

    bookings = get_bookings()
    available_seats = list(range(1,61))

    if bookings:
        for booking in bookings:
            for seat in range(1,61):
                if seat == int(booking[4]):
                    available_seats.remove(seat)

    return available_seats

def get_specific_booking_details(id):
    """Returns list variable with booking details of specified id"""

    allBookings = get_bookings()

    for booking in allBookings:
        if int(id) == int(booking[4]):
            return booking

# board and console

def get_bc_bookings():
    """Returns list of all bc_bookings"""
    
    # if development
    if config["development"]:
        return dev_bc_bookings
    else:
        return sql_query("SELECT * FROM bc_bookings")

def get_specific_bc_booking_details(id):
    """Returns list variable with bc_booking details of specified id"""

    allBookings = bc_get_bookings()

    for booking in allBookings:
        if int(id) == int(booking[4]):
            return booking

# error routes
@app.errorhandler(400)
def error_400(e):
    return jsonify({"status": False, "http_code": 400, "message": "Felaktig begäran.", "response": {}}), 400

@app.errorhandler(401)
def error_401(e):
    return jsonify({"status": False, "http_code": 401, "message": "Åtkomst nekas.", "response": {}}), 401

@app.errorhandler(404)
def error_404(e):
    return jsonify({"status": False, "http_code": 404, "message": "Resursen du söker hittades inte.", "response": {}}), 404

@app.errorhandler(405)
def error_405(e):
    return jsonify({"status": False, "http_code": 405, "message": "Felaktig begäran, ej tillåten metod.", "response": {}}), 405

@app.errorhandler(500)
def error_500(e):
    return jsonify({"status": False, "http_code": 500, "message": "Internt serverfel inträffade.", "response": {}}), 500

# application routes
@app.route(f"{BASEPATH}/info", methods=["GET"])
@disable_check
def info():
    return jsonify({
        "status": True,
        "http_code": 200,
        "message": "request successful",
        "response": {
            "version": version,
            "event_date": config["event_date"],
            "development_mode": config["development"],
            "int_available_seats": int(len(get_available_seats_list())),
            "int_booked_seats": int(len(get_bookings()))
        }
    })

@app.route(f"{BASEPATH}/auth", methods=["POST"])
@disable_check
def auth():
    if request.json["password"] == config["lock_password"]:
        clear_old_sessions()
        token = new_session()

        if token != False:
            return jsonify({
                "status": True,
                "http_code": 200,
                "message": "request successful",
                "response": {
                    "session": token
                }
            })
        else:
            return error_500(None), 500
    
    return jsonify({
        "status": False,
        "http_code": 401,
        "message": "Felaktigt lösenord.",
        "response": {}
    })

@app.route(f"{BASEPATH}/bookings", methods=["POST"])
@disable_check
@auth_required
def bookings():
    bookings = get_bookings()        

    return jsonify({
        "status": True,
        "http_code": 200,
        "message": "request successful",
        "response": {
            "bookings": bookings
        },
    })

@app.route(f"{BASEPATH}/bookings/<id>", methods=["POST"])
@disable_check
@auth_required
def booking(id):
    if not is_integer(id):
        return error_400(None), 400

    booking = get_specific_booking_details(id)        

    return jsonify({
        "status": True,
        "http_code": 200,
        "message": "request successful",
        "response": {
            "booking": booking
        },
    })

@app.route(f"{BASEPATH}/book", methods=["POST"])
@disable_check
@auth_required
def book():
    return jsonify({
        "status": True,
        "http_code": 200,
        "message": "request successful",
        "response": {}
    }) 

# board and console

@app.route(f"{BASEPATH}/bc/bookings", methods=["POST"])
@disable_check
@auth_required
def bc_bookings():
    bookings = get_bc_bookings()        

    return jsonify({
        "status": True,
        "http_code": 200,
        "message": "request successful",
        "response": {
            "bookings": bookings
        },
    })

@app.route(f"{BASEPATH}/bc/bookings/<id>", methods=["POST"])
@disable_check
@auth_required
def bc_booking(id):
    if not is_integer(id):
        return error_400(None), 400

    booking = get_specific_bc_booking_details(id)        

    return jsonify({
        "status": True,
        "http_code": 200,
        "message": "request successful",
        "response": {
            "booking": booking
        },
    })

@app.route(f"{BASEPATH}/bc/book", methods=["POST"])
@disable_check
@auth_required
def bc_book():
    return jsonify({
        "status": True,
        "http_code": 200,
        "message": "request successful",
        "response": {}
    })

# run application
if __name__ == '__main__':
    app.run(host='0.0.0.0')