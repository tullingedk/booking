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

from flask import Flask, render_template, request, redirect, make_response, session, send_file
from functools import wraps
from db import *
import string

# Session Imports
from flask_session.__init__ import Session
from datetime import timedelta, datetime

app = Flask(__name__)

import random
import string
import json

import os.path

from version import version
from swish_qr_generator import generate_swish_qr

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# variables
if os.path.exists("override.config.json"):
    with open("override.config.json", 'r') as f:
        config = json.load(f)
else:
    with open("config.json", 'r') as f:
        config = json.load(f)

# illegal and legal characters
ILLEGAL_CHARACTERS = ["<", ">", ";"]
LEGAL_CHARACTERS = list(string.ascii_letters) + list(string.digits) + list(string.whitespace) + ["å", "ä", "ö", "Å", "Ä", "Ö", "@", "."]

# Session Management
SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = config["session_path"]
SESSION_PERMANENT = True
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

app.config.from_object(__name__)
Session(app)

# print to user that we're running dev mode if we are
if config["development"]:
    print("Booking system is running in development mode")

# devevlopment, define bookings as lists
dev_bookings = [["Test", "User", "TE18", "foo", 1, 1, "2019 yeet"]]
dev_bc_bookings = [["BC Test", "User", "TE18", "foo", 1, 1, "2002 yeet"]]

# decorators
def disable_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # check if system is disabled
        if config["disabled"] == True:
            return render_template("disabled.html", development_mode=config["development"], version=version)
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):        
        # check if logged in
        if session.get("user_login") != True:
            wrongPassword = request.args.get("wrongPassword")
            return render_template("lock.html", wrongPassword=wrongPassword, development_mode=config["development"], version=version, original_request_path=request.path)
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # check if user has admin session status
        if session.get("admin_login") != True:
            # simple admin page, won't bother for anything fancy
            wrongPassword = request.args.get("wrongPassword")
        
            return render_template("admin_login.html", development_mode=config["development"], version=version, wrongPassword=wrongPassword)
        return f(*args, **kwargs)
    return decorated_function

# functions
def is_integer(variable):
    """Returns boolean, True if variable is int and False if variable is not int"""

    try:
        check_integer = int(variable)
    except Exception:
        return False
    
    return True

#####################
# BOOKING FUNCTIONS #
#####################
def get_bookings():
    """Returns list of all bookings"""

    if config["development"]:
        return dev_bookings
    else:
        return sql_query("SELECT * FROM bookings")

def get_available_seats_list():
    """Returns list of available booking seats"""

    allBookings = get_bookings()
    available_seats = list(range(1,61))

    if allBookings:
        for booking in allBookings:
            for seat in range(1,61):
                if seat == int(booking[4]):
                    available_seats.remove(seat)

    return available_seats


def new_booking(firstname, lastname, school_class, email, seat):
    """Creates new booking using input variables"""

    bookings = get_bookings()

    already_used = False
    seat_taken = False
    for booking in bookings:
        if booking[3] == email:
            already_used = True
        if int(booking[4]) == int(seat):
            seat_taken = True

    if already_used or seat_taken:
        return False

    insert_booking = ("INSERT INTO bookings "
              "(firstname, lastname, school_class, email, seat, status, date) "
            """VALUES ('""" + firstname + """', '""" + lastname + """', '""" + school_class + """', '""" + email + """', '""" + seat + """', '1', CURRENT_TIMESTAMP())""")

    # if development
    if config["development"]:
        dev_bookings.append([firstname, lastname, school_class, email, seat, 1])
    else:
        try:
            result = sql_query(insert_booking)
        except Exception:
            return False

    return True

def get_specific_booking_details(id):
    """Returns list variable with booking details of specified id"""

    allBookings = get_bookings()

    for booking in allBookings:
        if int(id) == int(booking[4]):
            return booking

#####################################
## BOARD GAMES AND CONSOLE PLAYERS ##
#####################################
def bc_get_bookings():
    """Returns list of all bc_bookings"""
    
    # if development
    if config["development"]:
        return dev_bc_bookings
    else:
        return sql_query("SELECT * FROM bc_bookings")

def bc_get_available_seats_list():
    """Returns list of available bc_booking seats"""
    
    allBookings = bc_get_bookings()
    available_seats = list(range(1,11))

    if allBookings:
        for booking in allBookings:
            for seat in range(1,11):
                if seat == int(booking[4]):
                    available_seats.remove(seat)

    return available_seats


def bc_new_booking(firstname, lastname, school_class, email, seat):
    """Creates new bc_booking using input variables"""

    bookings = bc_get_bookings()

    already_used = False
    seat_taken = False
    for booking in bookings:
        if booking[3] == email:
            already_used = True
        if int(booking[4]) == int(seat):
            seat_taken = True

    if already_used or seat_taken:
        return False

    insert_booking = ("INSERT INTO bc_bookings "
              "(firstname, lastname, school_class, email, seat, status, date) "
            """VALUES ('""" + firstname + """', '""" + lastname + """', '""" + school_class + """', '""" + email + """', '""" + seat + """', '1', CURRENT_TIMESTAMP())""")

    # if development
    if config["development"]:
        dev_bc_bookings.append([firstname, lastname, school_class, email, seat, 1])
    else:
        try:
            result = sql_query(insert_booking)
        except Exception:
            return False

    return True

def bc_get_specific_booking_details(id):
    """Returns list variable with bc_booking details of specified id"""

    allBookings = bc_get_bookings()

    for booking in allBookings:
        if int(id) == int(booking[4]):
            return booking

#################
## MAIN ROUTES ##
#################
@app.route("/")
@disable_check
@login_required
def index_page():
    # page generation date
    page_generation_date = datetime.now()

    # request arguments
    success = request.args.get("success")
    fail = request.args.get("fail")
    boka = request.args.get("boka")
    bc_boka = request.args.get("bc_boka")
    id = request.args.get("id")
    bc_id = request.args.get("bc_id")
    swish_qr = request.args.get("swish_qr")

    # show information about specific booking by id
    id_name = None
    id_class = None
    id_status = None
    id_date = None
    id_paid = False
    if id and is_integer(id):
        clicked_booking = get_specific_booking_details(id)
        if clicked_booking != None:
            id_name = clicked_booking[0] + " " + clicked_booking[1]
            id_class = clicked_booking[2]
            if clicked_booking[5] == 0:
                id_status = """Betald"""
                id_paid = True
            else:
                id_status = """Ej betald"""
            id_date = clicked_booking[6]
        else:
            # set id to False, site will not show modal
            id = False
    else:
        id = False

    # show information about specific bc_booking by bc_id
    bc_id_name = None
    bc_id_class = None
    bc_id_status = None
    bc_id_date = None
    bc_id_paid = False
    if bc_id and is_integer(bc_id):
        clicked_booking = bc_get_specific_booking_details(bc_id)
        if clicked_booking != None:
            bc_id_name = clicked_booking[0] + " " + clicked_booking[1]
            bc_id_class = clicked_booking[2]
            if clicked_booking[5] == 0:
                bc_id_status = """Betald"""
                bc_id_paid = True
            else:
                bc_id_status = """Ej betald"""
            bc_id_date = clicked_booking[6]
        else:
            # set bc_id to False, site will not show modal
            bc_id = False
    else:
        bc_id = False

    available_seats = get_available_seats_list()
    bc_available_seats = bc_get_available_seats_list()

    # bookings
    bookings = get_bookings()
    booked_ids = []
    for booking in bookings:
        booked_ids.append([booking[4], booking[5]])

    bc_bookings = bc_get_bookings()
    bc_booked_ids = []
    for bc_booking in bc_bookings:
        bc_booked_ids.append([bc_booking[4], bc_booking[5]])

    # for att kunna visa antalet lediga platser
    num_available_seats = len(available_seats)
    num_bookings = len(bookings)

    return render_template("index.html", success=success, fail=fail, boka=boka, bc_boka=bc_boka, swish_qr=swish_qr, all_seats=range(1,61), bc_all_seats=range(1,11), num_all_seats=len(range(1,61)), id=id, booked_ids=booked_ids, bc_booked_ids=bc_booked_ids, available_seats=available_seats, bc_available_seats=bc_available_seats, id_name=id_name, id_class=id_class, id_status=id_status, id_date=id_date, bc_id=bc_id, bc_id_name=bc_id_name, bc_id_class=bc_id_class, bc_id_status=bc_id_status, bc_id_date=bc_id_date, num_available_seats=num_available_seats, num_bookings=num_bookings, id_paid=id_paid, bc_id_paid=bc_id_paid, event_date=config["event_date"], development_mode=config["development"], version=version, page_generation_date=page_generation_date)

@app.route("/info")
@disable_check
@login_required
def info_page():
    return render_template("info.html", event_date=config["event_date"])

@app.route("/maserati/admin")
@disable_check
@admin_required
def admin_page():
    success = request.args.get("success")
    fail = request.args.get("fail")
    id = request.args.get("id")
    bc_id = request.args.get("bc_id")

    # get specific id
    id_name = None
    id_class = None
    id_status = None
    id_date = None
    if id:
        clicked_booking = get_specific_booking_details(id)
        id_name = clicked_booking[0] + " " + clicked_booking[1]
        id_class = clicked_booking[2]
        if clicked_booking[5] == 0:
            id_status = """Betald"""
        else:
            id_status = """Ej betald"""
        id_date = clicked_booking[6]

    # get specific bc id
    bc_id_name = None
    bc_id_class = None
    bc_id_status = None
    bc_id_date = None
    if bc_id:
        clicked_booking = bc_get_specific_booking_details(bc_id)
        bc_id_name = clicked_booking[0] + " " + clicked_booking[1]
        bc_id_class = clicked_booking[2]
        if clicked_booking[5] == 0:
            bc_id_status = """Betald"""
        else:
            bc_id_status = """Ej betald"""
        bc_id_date = clicked_booking[6]


    available_seats = get_available_seats_list()
    bc_available_seats = bc_get_available_seats_list()

    # bookings
    bookings = get_bookings()
    booked_ids = []
    for booking in bookings:
        booked_ids.append([booking[4], booking[5]])

    bc_bookings = bc_get_bookings()
    bc_booked_ids = []
    for bc_booking in bc_bookings:
        bc_booked_ids.append([bc_booking[4], bc_booking[5]])

    return render_template("admin.html", success=success, fail=fail, all_seats=range(1,61), bc_all_seats=range(1,11), num_all_seats=len(range(1,61)), id=id, booked_ids=booked_ids, bc_booked_ids=bc_booked_ids, available_seats=available_seats, bc_available_seats=bc_available_seats, id_name=id_name, id_class=id_class, id_status=id_status, id_date=id_date, bc_id=bc_id, bc_id_name=bc_id_name, bc_id_class=bc_id_class, bc_id_status=bc_id_status, bc_id_date=bc_id_date, development_mode=config["development"])

################
## API ROUTES ##
################
@app.route("/api/lockpassword", methods=["POST"])
@disable_check
def api_lockpassword():
    password = request.form.get("password")
    original_request_path = request.form.get("original_request_path")

    if password == config["lock_password"]:
        # set user_login as True in the users active session
        session["user_login"] = True
        print("{}".format(original_request_path))
        return redirect("{}".format(original_request_path))
    else:
        return redirect("{}?wrongPassword=true".format(original_request_path))

@app.route("/api/admin/login", methods=["POST"])
@disable_check
def api_admin_login():
    password = request.form.get("password")

    # simple admin page
    if password == config["admin_password"]:
        session["admin_login"] = True

        return redirect("/maserati/admin")

    return redirect("/maserati/admin?wrongPassword=true")

@app.route("/api/admin/logout")
@disable_check
def api_admin_logout():
    # pop session
    session.pop("admin_login", None)
    return redirect("/")

@app.route("/api/admin/set/booking/paid/<id>")
@disable_check
@admin_required
def api_admin_set_booking_paid(id):
    if config["development"]:
        global dev_bookings
        dev_bookings = [["Test", "User", "TE18", "woo", 1, 0, "2019 yeet"]]
    else:
        sql_query("""UPDATE bookings SET status = 0 WHERE seat=""" + str(id))
    return redirect("/maserati/admin?id=" + str(id))

@app.route("/api/admin/set/booking/unpaid/<id>")
@disable_check
@admin_required
def api_admin_set_booking_unpaid(id):
    if config["development"]:
        global dev_bookings
        dev_bookings = [["Test", "User", "TE18", "woo", 1, 1, "2019 yeet"]]
    else:
        sql_query("""UPDATE bookings SET status = 1 WHERE seat=""" + str(id))
    return redirect("/maserati/admin?id=" + str(id))

@app.route("/api/admin/set/bc_booking/paid/<id>")
@disable_check
@admin_required
def api_admin_set_bc_booking_paid(id):
    if config["development"]:
        global dev_bc_bookings
        dev_bc_bookings = [["BC Test", "User", "TE18", "woo", 1, 0, "2002 yeet"]]
    else:
        sql_query("""UPDATE bc_bookings SET status = 0 WHERE seat=""" + str(id))
    return redirect("/maserati/admin?bc_id=" + str(id))

@app.route("/api/admin/set/bc_booking/unpaid/<id>")
@disable_check
@admin_required
def api_admin_set_bc_booking_unpaid(id):
    if config["development"]:
        global dev_bc_bookings
        dev_bc_bookings = [["BC Test", "User", "TE18", "woo", 1, 1, "2002 yeet"]]
    else:
        sql_query("""UPDATE bc_bookings SET status = 1 WHERE seat=""" + str(id))
    return redirect("/maserati/admin?bc_id=" + str(id))

@app.route("/api/book", methods=["POST"])
@disable_check
@login_required
def api_book():
    validation = True

    # check if only valid keys were sent
    for key, value in request.form.items():
        if key != "firstname" and key != "lastname" and key != "school_class" and key != "email" and key != "seat":
            return redirect("/?fail=true")

        if len(value) < 3 or len(value) > 50:
            if key != "seat":
                print(key)
                print(value)
                validation = False

    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    school_class = request.form["school_class"]
    email = request.form["email"]
    seat = request.form["seat"]

    if is_integer(seat) != True:
        validation = False

    all_input_variables = firstname + lastname + school_class + email + seat
    if any(x in all_input_variables for x in ILLEGAL_CHARACTERS):
        validation = False

    # check for legal characters
    if any(x not in LEGAL_CHARACTERS for x in all_input_variables):
        validation = False
    
    if "@skola.botkyrka.se" not in email:
        validation = False

    if validation == False:
        return redirect("/?fail=true")

    if new_booking(firstname, lastname, school_class, email, seat) and validation:
        return redirect("/?success=true&id={}".format(str(seat)))
    else:
        return redirect("/?fail=true")

@app.route("/api/bc_book", methods=["POST"])
@disable_check
@login_required
def bc_api_book():
    validation = True

    # check if only valid keys were sent
    for key, value in request.form.items():
        if key != "firstname" and key != "lastname" and key != "school_class" and key != "email" and key != "seat":
            return redirect("/?fail=true")

        if len(value) < 3 or len(value) > 50:
            if key != "seat":
                print(key)
                print(value)
                validation = False

    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    school_class = request.form["school_class"]
    email = request.form["email"]
    seat = request.form["seat"]

    if is_integer(seat) != True:
        validation = False

    all_input_variables = firstname + lastname + school_class + email + seat
    if any(x in all_input_variables for x in ILLEGAL_CHARACTERS):
        validation = False

    # check for legal characters
    if any(x not in LEGAL_CHARACTERS for x in all_input_variables):
        validation = False
    
    if "@skola.botkyrka.se" not in email:
        validation = False

    if validation == False:
        return redirect("/?fail=true")

    if bc_new_booking(firstname, lastname, school_class, email, seat) and validation:
        return redirect("/?success=true&bc_id={}".format(str(seat)))
    else:
        return redirect("/?fail=true")

@app.route("/api/swish/booking/qr/<id>")
@disable_check
@login_required
def api_swish_booking_qr(id):
    # get specific id
    id_firstname = None
    id_lastname = None
    id_class = None
    if id and is_integer(id):
        clicked_booking = get_specific_booking_details(id)

        if clicked_booking != None:
            id_firstname = clicked_booking[0]
            id_lastname = clicked_booking[1]
            id_class = clicked_booking[2]

            generate_swish_qr(id_firstname, id_lastname, id_class, 0) # 0 means status unpaid

            return send_file("static/temp_swish.png", mimetype="image/png")
        return "booking id does not exist", 400
    return "id not defined or id not integer", 400

@app.route("/api/swish/bc_booking/qr/<id>")
@disable_check
@login_required
def api_swish_bc_booking_qr(id):
    # get specific id
    id_firstname = None
    id_lastname = None
    id_class = None
    if id and is_integer(id):
        clicked_booking = bc_get_specific_booking_details(id)

        if clicked_booking != None:
            id_firstname = clicked_booking[0]
            id_lastname = clicked_booking[1]
            id_class = clicked_booking[2]

            generate_swish_qr(id_firstname, id_lastname, id_class, 1)

            return send_file("static/temp_swish.png", mimetype="image/png")
        return "booking bc_id does not exist", 400
    return "id not defined or id not integer", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0')