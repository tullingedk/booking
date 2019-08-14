# Datorklubben Booking sytsem
# (c) Vilhelm Prytz 2019
# https://www.vilhelmprytz.se

from flask import Flask, render_template, request, redirect, make_response, session
from db import *

# Session Imports
from flask_session.__init__ import Session

app = Flask(__name__)

import random
import string
import json

import os.path

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

# Session Management
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

# print to user that we're running dev mode if we are
if config["development"]:
    print("RUNNING IN DEVELOPMENT MODE")

# BOOKINGS
# firstname
# lastname
# school_class
# email
# seat
# status
#       1: booked and paid
#       0: booked, not paid
# date

# dev
dev_bookings = [["Test", "User", "TE18", "woo", 1, 1, "2019 yeet"]]
dev_bc_bookings = [["BC Test", "User", "TE18", "woo", 1, 1, "2002 yeet"]]

# functions
def get_bookings():
    if config["development"]:
        return dev_bookings
    else:
        return sql_query("SELECT * FROM bookings")

def get_available_seats_list():
    allBookings = get_bookings()
    available_seats = range(1,61)

    if allBookings:
        for booking in allBookings:
            for seat in range(1,61):
                if seat == int(booking[4]):
                    available_seats.remove(seat)

    return available_seats


def new_booking(firstname, lastname, school_class, email, seat):
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
    allBookings = get_bookings()

    for booking in allBookings:
        if int(id) == int(booking[4]):
            return booking

#####################################
## BOARD GAMES AND CONSOLE PLAYERS ##
#####################################
def bc_get_bookings():
    # if development
    if config["development"]:
        return dev_bc_bookings
    else:
        return sql_query("SELECT * FROM bc_bookings")

def bc_get_available_seats_list():
    allBookings = bc_get_bookings()
    available_seats = range(1,11)

    if allBookings:
        for booking in allBookings:
            for seat in range(1,11):
                if seat == int(booking[4]):
                    available_seats.remove(seat)

    return available_seats


def bc_new_booking(firstname, lastname, school_class, email, seat):
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
    allBookings = bc_get_bookings()

    for booking in allBookings:
        if int(id) == int(booking[4]):
            return booking

#################
## MAIN ROUTES ##
#################
@app.route("/")
def index_page():
    if config["disabled"] == True:
        return render_template("disabled.html")

    if session.get("user_login") == True:
        success = request.args.get("success")
        fail = request.args.get("fail")
        boka = request.args.get("boka")
        bc_boka = request.args.get("bc_boka")
        id = request.args.get("id")
        bc_id = request.args.get("bc_id")
        swish_qr = request.args.get("swish_qr")

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

        # for att kunna visa antalet lediga platser
        num_available_seats = len(available_seats)
        num_bookings = len(bookings)

        return render_template("index.html", success=success, fail=fail, boka=boka, bc_boka=bc_boka, swish_qr=swish_qr, all_seats=range(1,61), bc_all_seats=range(1,11), num_all_seats=len(range(1,61)), id=id, booked_ids=booked_ids, bc_booked_ids=bc_booked_ids, available_seats=available_seats, bc_available_seats=bc_available_seats, id_name=id_name, id_class=id_class, id_status=id_status, id_date=id_date, bc_id=bc_id, bc_id_name=bc_id_name, bc_id_class=bc_id_class, bc_id_status=bc_id_status, bc_id_date=bc_id_date, num_available_seats=num_available_seats, num_bookings=num_bookings, event_date=config["event_date"], development_mode=config["development"])
    else:
        wrongPassword = request.args.get("wrongPassword")
        return render_template("lock.html", wrongPassword=wrongPassword)

@app.route("/info")
def info_page():
    if config["disabled"] == True:
        return render_template("disabled.html")
    return render_template("info.html", event_date=config["event_date"])

@app.route("/maserati/admin")
def admin_page():
    if session.get("admin_login") == True:
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
    else:
        return """<p>Login</p> <form action="/api/admin/unlock"><input type="password" name="password" required><input type="submit" value="Skicka"></form>"""

################
## API ROUTES ##
################
@app.route("/api/lockpassword")
def api_lockpassword():
    if config["disabled"] == True:
        return render_template("disabled.html")
    password = request.args.get("password")

    if password == config["lock_password"]:
        session["user_login"] = True
        return redirect("/")
    else:
        return redirect("/?wrongPassword=true")

@app.route("/api/admin/unlock")
def api_admin_unlock():
    password = request.args.get("password")
    if password == config["admin_password"]:
        session["admin_login"] = True

    return redirect("/maserati/admin")


@app.route("/api/book")
def api_book():
    if config["disabled"] == True:
        return render_template("disabled.html")
    if session.get("user_login") == True:
        firstname = request.args.get("firstname")
        lastname = request.args.get("lastname")
        school_class = request.args.get("school_class")
        email = request.args.get("email")
        seat = request.args.get("seat")

        blocked = ["<", ">"]

        validation = True
        if any(x in firstname for x in blocked) or any(x in lastname for x in blocked) or any(x in school_class for x in blocked) or any(x in email for x in blocked) or any(x in seat for x in blocked):
            validation = False

        if "@skola.botkyrka.se" not in email:
            validation = False

        if validation == False:
            return redirect("/?fail=true")

        if new_booking(firstname, lastname, school_class, email, seat) and validation:
            return redirect("/?success=true")
        else:
            return redirect("/?fail=true")
    else:
        wrongPassword = request.args.get("wrongPassword")
        return render_template("lock.html", wrongPassword=wrongPassword)

@app.route("/api/bc_book")
def bc_api_book():
    if config["disabled"] == True:
        return render_template("disabled.html")
    if session.get("user_login") == True:
        firstname = request.args.get("firstname")
        lastname = request.args.get("lastname")
        school_class = request.args.get("school_class")
        email = request.args.get("email")
        seat = request.args.get("seat")

        blocked = ["<", ">"]

        validation = True
        if any(x in firstname for x in blocked) or any(x in lastname for x in blocked) or any(x in school_class for x in blocked) or any(x in email for x in blocked) or any(x in seat for x in blocked):
            validation = False

        if "@skola.botkyrka.se" not in email:
            validation = False

        if validation == False:
            return redirect("/?fail=true")

        if bc_new_booking(firstname, lastname, school_class, email, seat) and validation:
            return redirect("/?success=true")
        else:
            return redirect("/?fail=true")
    else:
        wrongPassword = request.args.get("wrongPassword")
        return render_template("lock.html", wrongPassword=wrongPassword)
