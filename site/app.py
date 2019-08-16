# Datorklubben Booking sytsem
# (c) Vilhelm Prytz 2019
# https://www.vilhelmprytz.se

from flask import Flask, render_template, request, redirect, make_response, session, send_file
from db import *

# Session Imports
from flask_session.__init__ import Session
from datetime import timedelta

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

# Session Management
SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = config["session_path"]
SESSION_PERMANENT = True
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

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
#       0: booked and paid
#       1: booked, not paid
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
        return render_template("disabled.html", development_mode=config["development"], version=version)

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
        id_paid = False
        if id:
            clicked_booking = get_specific_booking_details(id)
            id_name = clicked_booking[0] + " " + clicked_booking[1]
            id_class = clicked_booking[2]
            if clicked_booking[5] == 0:
                id_status = """Betald"""
                id_paid = True
            else:
                id_status = """Ej betald"""
            id_date = clicked_booking[6]

        # get specific bc id
        bc_id_name = None
        bc_id_class = None
        bc_id_status = None
        bc_id_date = None
        bc_id_paid = False
        if bc_id:
            clicked_booking = bc_get_specific_booking_details(bc_id)
            bc_id_name = clicked_booking[0] + " " + clicked_booking[1]
            bc_id_class = clicked_booking[2]
            if clicked_booking[5] == 0:
                bc_id_status = """Betald"""
                bc_id_paid = True
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

        return render_template("index.html", success=success, fail=fail, boka=boka, bc_boka=bc_boka, swish_qr=swish_qr, all_seats=range(1,61), bc_all_seats=range(1,11), num_all_seats=len(range(1,61)), id=id, booked_ids=booked_ids, bc_booked_ids=bc_booked_ids, available_seats=available_seats, bc_available_seats=bc_available_seats, id_name=id_name, id_class=id_class, id_status=id_status, id_date=id_date, bc_id=bc_id, bc_id_name=bc_id_name, bc_id_class=bc_id_class, bc_id_status=bc_id_status, bc_id_date=bc_id_date, num_available_seats=num_available_seats, num_bookings=num_bookings, id_paid=id_paid, bc_id_paid=bc_id_paid, event_date=config["event_date"], development_mode=config["development"], version=version)
    else:
        wrongPassword = request.args.get("wrongPassword")
        return render_template("lock.html", wrongPassword=wrongPassword, development_mode=config["development"], version=version)

@app.route("/info")
def info_page():
    if config["disabled"] == True:
        return render_template("disabled.html", development_mode=config["development"], version=version)
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
        return render_template("disabled.html", development_mode=config["development"], version=version)
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

@app.route("/api/admin/logout")
def api_admin_logout():
    session.pop("admin_login", None)
    return redirect("/")

@app.route("/api/admin/set/booking/paid/<id>")
def api_admin_set_booking_paid(id):
    if session.get("admin_login") == True:
        if config["development"]:
            global dev_bookings
            dev_bookings = [["Test", "User", "TE18", "woo", 1, 0, "2019 yeet"]]
        else:
            sql_query("""UPDATE bookings SET status = 0 WHERE seat=""" + str(id))
        return redirect("/maserati/admin?id=" + str(id))
    else:
        return redirect("/maserati/admin")

@app.route("/api/admin/set/booking/unpaid/<id>")
def api_admin_set_booking_unpaid(id):
    if session.get("admin_login") == True:
        if config["development"]:
            global dev_bookings
            dev_bookings = [["Test", "User", "TE18", "woo", 1, 1, "2019 yeet"]]
        else:
            sql_query("""UPDATE bookings SET status = 1 WHERE seat=""" + str(id))
        return redirect("/maserati/admin?id=" + str(id))
    else:
        return redirect("/maserati/admin")

@app.route("/api/admin/set/bc_booking/paid/<id>")
def api_admin_set_bc_booking_paid(id):
    if session.get("admin_login") == True:
        if config["development"]:
            global dev_bc_bookings
            dev_bc_bookings = [["BC Test", "User", "TE18", "woo", 1, 0, "2002 yeet"]]
        else:
            sql_query("""UPDATE bc_bookings SET status = 0 WHERE seat=""" + str(id))
        return redirect("/maserati/admin?bc_id=" + str(id))
    else:
        return redirect("/maserati/admin")

@app.route("/api/admin/set/bc_booking/unpaid/<id>")
def api_admin_set_bc_booking_unpaid(id):
    if session.get("admin_login") == True:
        if config["development"]:
            global dev_bc_bookings
            dev_bc_bookings = [["BC Test", "User", "TE18", "woo", 1, 1, "2002 yeet"]]
        else:
            sql_query("""UPDATE bc_bookings SET status = 1 WHERE seat=""" + str(id))
        return redirect("/maserati/admin?bc_id=" + str(id))
    else:
        return redirect("/maserati/admin")

@app.route("/api/book")
def api_book():
    if config["disabled"] == True:
        return render_template("disabled.html", development_mode=config["development"], version=version)
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
        return render_template("lock.html", wrongPassword=wrongPassword, development_mode=config["development"], version=version)

@app.route("/api/bc_book")
def bc_api_book():
    if config["disabled"] == True:
        return render_template("disabled.html", development_mode=config["development"], version=version)
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
        return render_template("lock.html", wrongPassword=wrongPassword, development_mode=config["development"], version=version)

@app.route("/api/swish/booking/qr/<id>")
def api_swish_booking_qr(id):
    # get specific id
    id_firstname = None
    id_lastname = None
    id_class = None
    if id:
        clicked_booking = get_specific_booking_details(id)
        id_firstname = clicked_booking[0]
        id_lastname = clicked_booking[1]
        id_class = clicked_booking[2]

        generate_swish_qr(id_firstname, id_lastname, id_class, 0)

        return send_file("static/temp_swish.png", mimetype="image/png")

@app.route("/api/swish/bc_booking/qr/<id>")
def api_swish_bc_booking_qr(id):
    # get specific id
    id_firstname = None
    id_lastname = None
    id_class = None
    if id:
        clicked_booking = bc_get_specific_booking_details(id)
        id_firstname = clicked_booking[0]
        id_lastname = clicked_booking[1]
        id_class = clicked_booking[2]

        generate_swish_qr(id_firstname, id_lastname, id_class, 1)

        return send_file("static/temp_swish.png", mimetype="image/png")