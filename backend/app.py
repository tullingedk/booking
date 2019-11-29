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

import os.path
import string

from db import *
from decorators import *
# imports
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from session import *
from swish_qr_generator import generate_swish_qr
from tools import *
from version import commit_hash, version

# variables
ILLEGAL_CHARACTERS = ["<", ">", ";"]
ALLOWED_CHARACTERS = list(string.printable) + ["å", "ä", "ö", "Å", "Ä", "Ö"]

BASEPATH = "/backend"
NUM_TOTAL_SEATS=48
NUM_TOTAL_BC_SEATS=10

# configuration
if os.path.exists("override.config.json"):
    with open("override.config.json", 'r') as f:
        config = json.load(f)
else:
    with open("config.json", 'r') as f:
        config = json.load(f)

# validate some configuration values
if len(config["lock_password"]) < 3 or len(config["lock_password"]) > 200 or len(config["admin_password"]) < 3 or len(config["admin_password"]) > 200:
    raise Exception("passwords should be 3 to 200 characters long")

# flask application
app = Flask(__name__)
CORS(app)

# functions
def get_bookings():
    """Returns list of all bookings"""

    return sql_query("SELECT * FROM bookings")

def get_available_seats_list():
    """Returns list of available booking seats"""

    bookings = get_bookings()
    available_seats = list(range(1,NUM_TOTAL_SEATS+1))

    if bookings:
        for booking in bookings:
            for seat in range(1,NUM_TOTAL_SEATS+1):
                if seat == int(booking[3]):
                    available_seats.remove(seat)

    return available_seats

def get_specific_booking_details(id):
    """Returns list variable with booking details of specified id"""

    allBookings = get_bookings()

    for booking in allBookings:
        if int(id) == int(booking[3]):
            return booking

# board and console
def get_bc_bookings():
    """Returns list of all bc_bookings"""
    
    return sql_query("SELECT * FROM bc_bookings")

def bc_get_available_seats_list():
    """Returns list of available bc_booking seats"""
    
    bookings = get_bc_bookings()
    available_seats = list(range(1,NUM_TOTAL_BC_SEATS+1))

    if bookings:
        for booking in bookings:
            for seat in range(1,NUM_TOTAL_BC_SEATS+1):
                if seat == int(booking[3]):
                    available_seats.remove(seat)

    return available_seats

def get_specific_bc_booking_details(id):
    """Returns list variable with bc_booking details of specified id"""

    allBookings = get_bc_bookings()

    for booking in allBookings:
        if int(id) == int(booking[3]):
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
def info():
    return jsonify({
        "status": True,
        "http_code": 200,
        "message": "request successful",
        "response": {
            "version": version,
            "commit_hash": commit_hash[0:6],
            "disabled": config["disabled"],
            "event_date": config["event_date"],
            "int_available_seats": int(len(get_available_seats_list())),
            "int_booked_seats": int(len(get_bookings()))
        }
    })

@app.route(f"{BASEPATH}/auth", methods=["POST"])
@disable_check
def auth():
    # check for invalid length
    if len(request.json["password"]) < 3 or len(request.json["password"]) > 200:
        return jsonify({
            "status": False,
            "http_code": 400,
            "message": "invalid password length (3 to 200 characters)",
            "response": {}
        }), 400

    if request.json["password"] == config["lock_password"]:
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            remote_ip = request.environ['REMOTE_ADDR']
        else:
            remote_ip = request.environ['HTTP_X_FORWARDED_FOR']
        
        clear_old_sessions()
        token = new_session(remote_ip, is_admin=False)

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

@app.route(f"{BASEPATH}/validate_session", methods=["POST"])
@disable_check
@auth_required
def validate_session():
    # get user session
    session = get_session(request.json["token"])

    # if come this far, user would be authenticated
    return jsonify({
        "status": True,
        "http_code": 200,
        "message": "valid session",
        "response": {
            "is_admin": session[3]
        }
    })

@app.route(f"{BASEPATH}/logout", methods=["POST"])
@disable_check
@auth_required
def logout():
    # get user session
    session = get_session(request.json["token"])

    if destroy_session(request.json["token"]):
        return jsonify({
            "status": True,
            "http_code": 200,
            "message": "session destroyed",
            "response": {}
        })
    
    return jsonify({
        "status": False,
        "http_code": 500,
        "message": "Internal server error - unable to destroy session",
        "response": {}
    }), 500

# bookings
@app.route(f"{BASEPATH}/bookings", methods=["POST"])
@disable_check
@auth_required
def bookings():
    bookings_raw = get_bookings()
    bookings = []

    for booking in bookings_raw:
        bookings.append({
            "id": booking[3],
            "name": booking[0],
            "school_class": booking[1],
            "status": booking[4],
            "date": str(booking[5])
        })

    return jsonify({
        "status": True,
        "http_code": 200,
        "message": "request successful",
        "response": {
            "bookings": bookings
        },
    })

@app.route(f"{BASEPATH}/available_seat_list", methods=["POST"])
@disable_check
@auth_required
def available_seat_list():
    available_seat_list = get_available_seats_list()

    return jsonify({
        "status": True,
        "http_code": 200,
        "message": "request successful",
        "response": {
            "available_seat_list": available_seat_list
        }
    })

@app.route(f"{BASEPATH}/book", methods=["POST"])
@disable_check
@auth_required
def book():
    if request.headers["content-type"] == "application/json":
        form_data = request.json

        # combine all input data and check for illegal characters and allowed characters
        all_input_data = ''
        for key, value in form_data.items():
            all_input_data = all_input_data + str(key)
            all_input_data = all_input_data + str(value)

        # validate data
        if any(x in all_input_data for x in ILLEGAL_CHARACTERS):
            return jsonify({
                "status": False,
                "http_code": 400,
                "message": "Någon av skickade variabler innehåller explicit otillåtna tecken.",
                "response": {}
            }), 400

        if any(x not in ALLOWED_CHARACTERS for x in all_input_data):
            return jsonify({
                "status": False,
                "http_code": 400,
                "message": "Någon av skickade variabler innehåller okända tecken. Endast alfabetet och Å, Ä och Ö tillåts.",
                "response": {}
            }), 400

        # check data
        for key, value in form_data.items():
            # check for extra/invalid keys
            if len(form_data) != 5:
                return jsonify({
                    "status": False,
                    "http_code": 400,
                    "message": "Saknar variabler.",
                    "response": {}
                }), 400
            
            if key != "token" and key != "name" and key != "class" and key != "email" and key != "seat":
                return jsonify({
                    "status": False,
                    "http_code": 400,
                    "message": "invalid keys sent",
                    "response": {}
                }), 400

            # check for empty values
            if value == "":
                return jsonify({
                    "status": False,
                    "http_code": 400,
                    "message": f"{key} variabeln lämnades tom.",
                    "response": {}
                }), 400

            # check if values are too short or too long
            if len(str(value)) < 3 or len(str(value)) > 50 and key != "token":
                if key != "seat":
                    return jsonify({
                        "status": False,
                        "http_code": 400,
                        "message": f"{key} variabeln är för kort eller för lång (mellan 3 och 50 tecken).",
                        "response": {}
                    }), 400

            # check if class is too long
            if key == "class":
                if len(value) > 8:
                    return jsonify({
                        "status": False,
                        "http_code": 400,
                        "message": "Klass variabeln får max vara 8 karaktärer lång.",
                        "response": {}
                    }), 400

            # validate email
            if key == "email":
                if not "@skola.botkyrka.se" in value:
                    return jsonify({
                        "status": False,
                        "http_code": 400,
                        "message": "Ogiltig e-postadress. Du måste använda skolmailadressen.",
                        "response": {}
                    }), 400
            
            # check if seat is integer within range
            if key == "seat":
                if not is_integer(value):
                    return jsonify({
                        "status": False,
                        "http_code": 400,
                        "message": "seat must be integer",
                        "response": {}
                    }), 400

                if int(value) < 1 or int(value) > NUM_TOTAL_SEATS:
                    return jsonify({
                        "status": False,
                        "http_code": 400,
                        "message": "value is outside allowed range",
                        "response": {}
                    }), 400
        
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
            return jsonify({
                "status": False,
                "http_code": 400,
                "message": "Platsen du försöker boka är upptagen eller så har denna mailadress redan bokats av en annan plats.",
                "response": {}
            }), 400

        # if we've come this far, the input has then passed all validation

        # log ip
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            remote_ip = request.environ['REMOTE_ADDR']
        else:
            remote_ip = request.environ['HTTP_X_FORWARDED_FOR']

        # create booking
        insert_booking = f"""INSERT INTO bookings (name, school_class, email, seat, status, date, ip) VALUES ('{name}', '{school_class}', '{email}', {seat}, 1, CURRENT_TIMESTAMP(), '{remote_ip}')"""

        # insert
        try:
            sql_query(insert_booking)
        except Exception:
            return jsonify({
                "status": False,
                "http_code": 500,
                "message": "Ett internt serverfel inträffade när bokningen skulle sparas. Kontakta Prytz via Discord om problemet kvarstår.",
                "response": {}
            }), 500

        # successful
        return jsonify({
            "status": True,
            "http_code": 201,
            "message": "request successful",
            "response": {}
        }), 201

    # invalid content-type
    return jsonify({
        "status": False,
        "http_code": 400,
        "message": "invalid content type",
        "response": {}
    }), 400

@app.route(f"{BASEPATH}/swish/<id>", methods=["GET"])
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

            generate_swish_qr(name, school_class, seat, 0) # 0 means normal seat

            return send_file("static/temp_swish.png", mimetype="image/png")
        return jsonify({
            "status": False,
            "http_code": 400,
            "message": "id does not exist",
            "response": {}
        }), 400
    return jsonify({
        "status": False,
        "http_code": 400,
        "message": "id is not defined or not integer",
        "response": {}
    }), 400

# board and console
@app.route(f"{BASEPATH}/bc/bookings", methods=["POST"])
@disable_check
@auth_required
def bc_bookings():
    bookings_raw = get_bc_bookings()
    bookings = []

    for booking in bookings_raw:
        bookings.append({
            "id": booking[3],
            "name": booking[0],
            "school_class": booking[1],
            "status": booking[4],
            "date": str(booking[5])
        })

    return jsonify({
        "status": True,
        "http_code": 200,
        "message": "request successful",
        "response": {
            "bookings": bookings
        },
    })

@app.route(f"{BASEPATH}/bc/available_seat_list", methods=["POST"])
@disable_check
@auth_required
def bc_available_seat_list():
    available_seat_list = bc_get_available_seats_list()

    return jsonify({
        "status": True,
        "http_code": 200,
        "message": "request successful",
        "response": {
            "available_seat_list": available_seat_list
        }
    })

@app.route(f"{BASEPATH}/bc/book", methods=["POST"])
@disable_check
@auth_required
def bc_book():
    if request.headers["content-type"] == "application/json":
        form_data = request.json

        # combine all input data and check for illegal characters and allowed characters
        all_input_data = ''
        for key, value in form_data.items():
            all_input_data = all_input_data + str(key)
            all_input_data = all_input_data + str(value)

        # validate data
        if any(x in all_input_data for x in ILLEGAL_CHARACTERS):
            return jsonify({
                "status": False,
                "http_code": 400,
                "message": "Någon av skickade variabler innehåller explicit otillåtna tecken.",
                "response": {}
            }), 400

        if any(x not in ALLOWED_CHARACTERS for x in all_input_data):
            return jsonify({
                "status": False,
                "http_code": 400,
                "message": "Någon av skickade variabler innehåller okända tecken. Endast alfabetet och Å, Ä och Ö tillåts.",
                "response": {}
            }), 400

        # check data
        for key, value in form_data.items():
            # check for extra/invalid keys
            if len(form_data) != 5:
                return jsonify({
                    "status": False,
                    "http_code": 400,
                    "message": "Saknar variabler.",
                    "response": {}
                }), 400
            
            if key != "token" and key != "name" and key != "class" and key != "email" and key != "seat":
                return jsonify({
                    "status": False,
                    "http_code": 400,
                    "message": "invalid keys sent",
                    "response": {}
                }), 400

            # check for empty values
            if value == "":
                return jsonify({
                    "status": False,
                    "http_code": 400,
                    "message": f"{key} variabeln lämnades tom.",
                    "response": {}
                }), 400

            # check if values are too short or too long
            if len(str(value)) < 3 or len(str(value)) > 50 and key != "token":
                if key != "seat":
                    return jsonify({
                        "status": False,
                        "http_code": 400,
                        "message": f"{key} variabeln är för kort eller för lång (mellan 3 och 50 tecken).",
                        "response": {}
                    }), 400

            # check if class is too long
            if key == "class":
                if len(value) > 8:
                    return jsonify({
                        "status": False,
                        "http_code": 400,
                        "message": "Klass variabeln får max vara 8 karaktärer lång.",
                        "response": {}
                    }), 400

            # validate email
            if key == "email":
                if not "@skola.botkyrka.se" in value:
                    return jsonify({
                        "status": False,
                        "http_code": 400,
                        "message": "Ogiltig e-postadress. Du måste använda skolmailadressen.",
                        "response": {}
                    }), 400
            
            # check if seat is integer within range
            if key == "seat":
                if not is_integer(value):
                    return jsonify({
                        "status": False,
                        "http_code": 400,
                        "message": "seat must be integer",
                        "response": {}
                    }), 400

                if int(value) < 1 or int(value) > NUM_TOTAL_SEATS:
                    return jsonify({
                        "status": False,
                        "http_code": 400,
                        "message": "value is outside allowed range",
                        "response": {}
                    }), 400
        
        # check if seat is already booked or if this user has booked any other
        name = form_data["name"]
        school_class = form_data["class"].upper()
        email = form_data["email"]
        seat = form_data["seat"]

        already_used = False
        seat_taken = False
        for booking in get_bc_bookings():
            if booking[2] == email:
                already_used = True
            if int(booking[3]) == int(seat):
                seat_taken = True

        if already_used or seat_taken:
            return jsonify({
                "status": False,
                "http_code": 400,
                "message": "Platsen du försöker boka är upptagen eller så har denna mailadress redan bokats av en annan plats.",
                "response": {}
            }), 400

        # if we've come this far, the input has then passed all validation

        # log ip
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            remote_ip = request.environ['REMOTE_ADDR']
        else:
            remote_ip = request.environ['HTTP_X_FORWARDED_FOR']

        # create booking
        insert_booking = f"""INSERT INTO bc_bookings (name, school_class, email, seat, status, date, ip) VALUES ('{name}', '{school_class}', '{email}', {seat}, 1, CURRENT_TIMESTAMP(), '{remote_ip}')"""

        # insert
        try:
            sql_query(insert_booking)
        except Exception:
            return jsonify({
                "status": False,
                "http_code": 500,
                "message": "Ett internt serverfel inträffade när bokningen skulle sparas. Kontakta Prytz via Discord om problemet kvarstår.",
                "response": {}
            }), 500

        # successful
        return jsonify({
            "status": True,
            "http_code": 201,
            "message": "request successful",
            "response": {}
        }), 201

    # invalid content-type
    return jsonify({
        "status": False,
        "http_code": 400,
        "message": "invalid content type",
        "response": {}
    }), 400

@app.route(f"{BASEPATH}/bc/swish/<id>", methods=["GET"])
@disable_check
def bc_swish(id):
    # get specific id
    name = None
    school_class = None
    if id and is_integer(id):
        clicked_booking = get_specific_bc_booking_details(id)

        if clicked_booking != None:
            name = clicked_booking[0]
            school_class = clicked_booking[1]
            seat = clicked_booking[3]

            generate_swish_qr(name, school_class, seat, 1) # 1 means bc seat

            return send_file("static/temp_swish.png", mimetype="image/png")
        return jsonify({
            "status": False,
            "http_code": 400,
            "message": "id does not exist",
            "response": {}
        }), 400
    return jsonify({
        "status": False,
        "http_code": 400,
        "message": "id is not defined or not integer",
        "response": {}
    }), 400

# admin routes
@app.route(f"{BASEPATH}/admin/auth", methods=["POST"])
@disable_check
def admin_auth():
    # check for invalid length
    if len(request.json["password"]) < 3 or len(request.json["password"]) > 200:
        return jsonify({
            "status": False,
            "http_code": 400,
            "message": "invalid password length (3 to 200 characters)",
            "response": {}
        }), 400
    
    if request.json["password"] == config["admin_password"]:
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            remote_ip = request.environ['REMOTE_ADDR']
        else:
            remote_ip = request.environ['HTTP_X_FORWARDED_FOR']
        
        clear_old_sessions()
        token = new_session(remote_ip, is_admin=True)

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

@app.route(f"{BASEPATH}/admin/paid/<id>", methods=["POST"])
@disable_check
@admin_required
def admin_paid(id):
    if is_integer(id):
        booking = get_specific_booking_details(id)

        if booking != None:
            try:
                sql_query(f'UPDATE bookings SET status=0 WHERE seat={id}')
            except Exception:
                return jsonify({
                    "status": False,
                    "http_code": 500,
                    "message": "Ett internt serverfel inträffade.",
                    "response": {}
                }), 500

            return jsonify({
                "status": True,
                "http_code": 200,
                "message": "request successful",
                "response": {}
            })
        return jsonify({
            "status": False,
            "http_code": 400,
            "message": "Denna bokning existerar inte.",
            "response": {}
        }), 400
    
    return jsonify({
        "status": False,
        "http_code": 400,
        "message": "id must be integer",
        "response": {}
    }), 400

@app.route(f"{BASEPATH}/admin/unpaid/<id>", methods=["POST"])
@disable_check
@admin_required
def admin_unpaid(id):
    if is_integer(id):
        booking = get_specific_booking_details(id)

        if booking != None:
            try:
                sql_query(f'UPDATE bookings SET status=1 WHERE seat={id}')
            except Exception:
                return jsonify({
                    "status": False,
                    "http_code": 500,
                    "message": "Ett internt serverfel inträffade.",
                    "response": {}
                }), 500

            return jsonify({
                "status": True,
                "http_code": 200,
                "message": "request successful",
                "response": {}
            })
        return jsonify({
            "status": False,
            "http_code": 400,
            "message": "Denna bokning existerar inte.",
            "response": {}
        }), 400
    
    return jsonify({
        "status": False,
        "http_code": 400,
        "message": "id must be integer",
        "response": {}
    }), 400
@app.route(f"{BASEPATH}/admin/bc/paid/<id>", methods=["POST"])
@disable_check
@admin_required
def admin_bc_paid(id):
    if is_integer(id):
        booking = get_specific_bc_booking_details(id)

        if booking != None:
            try:
                sql_query(f'UPDATE bc_bookings SET status=0 WHERE seat={id}')
            except Exception:
                return jsonify({
                    "status": False,
                    "http_code": 500,
                    "message": "Ett internt serverfel inträffade.",
                    "response": {}
                }), 500

            return jsonify({
                "status": True,
                "http_code": 200,
                "message": "request successful",
                "response": {}
            })
        return jsonify({
            "status": False,
            "http_code": 400,
            "message": "Denna bokning existerar inte.",
            "response": {}
        }), 400
    
    return jsonify({
        "status": False,
        "http_code": 400,
        "message": "id must be integer",
        "response": {}
    }), 400

@app.route(f"{BASEPATH}/admin/bc/unpaid/<id>", methods=["POST"])
@disable_check
@admin_required
def admin_bc_unpaid(id):
    if is_integer(id):
        booking = get_specific_bc_booking_details(id)

        if booking != None:
            try:
                sql_query(f'UPDATE bc_bookings SET status=1 WHERE seat={id}')
            except Exception:
                return jsonify({
                    "status": False,
                    "http_code": 500,
                    "message": "Ett internt serverfel inträffade.",
                    "response": {}
                }), 500

            return jsonify({
                "status": True,
                "http_code": 200,
                "message": "request successful",
                "response": {}
            })
        return jsonify({
            "status": False,
            "http_code": 400,
            "message": "Denna bokning existerar inte.",
            "response": {}
        }), 400
    
    return jsonify({
        "status": False,
        "http_code": 400,
        "message": "id must be integer",
        "response": {}
    }), 400

# run application
if __name__ == '__main__':
    app.run(host='0.0.0.0')
