###########################################################################
#                                                                         #
# tullingedk/booking                                                      #
# Copyright (C) 2018 - 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                         #
# Licensed under the terms of the GNU GPL-3.0 license, see LICENSE.       #
# https://github.com/tullingedk/booking                                   #
#                                                                         #
###########################################################################

from flask import session, abort, Blueprint, request, send_file

from decorators.auth import google_logged_in, user_registered, is_admin
from validation import is_integer
from models import db, Booking, User, ConsoleBooking, Admin
from base import base_req
from swish import generate_swish_qr

booking_blueprint = Blueprint("booking", __name__, template_folder="../templates")

NUM_SEATS = 60
NUM_CONSOLE_SEATS = 20


@booking_blueprint.route("/bookings")
@google_logged_in
@user_registered
def bookings():
    bookings = Booking.query.all()
    console_bookings = ConsoleBooking.query.all()
    users = User.query.all()

    return base_req(
        response={
            "bookings": [
                {
                    "seat": booking.seat,
                    "name": booking.name,
                    "school_class": booking.school_class,
                    "email": None
                    if len(Admin.query.filter_by(email=session["google_email"]).all())
                    < 1
                    else booking.email,
                    "paid": booking.paid,
                    "picture_url": User.query.filter_by(email=booking.email)
                    .first()
                    .google_picture_url
                    if len(User.query.filter_by(email=booking.email).all()) != 0
                    else "",
                    "time_created": str(booking.time_created),
                    "time_updated": str(booking.time_updated),
                }
                for booking in bookings
            ],
            "console_bookings": [
                {
                    "seat": booking.seat,
                    "name": booking.name,
                    "school_class": booking.school_class,
                    "email": None
                    if len(Admin.query.filter_by(email=session["google_email"]).all())
                    < 1
                    else booking.email,
                    "paid": booking.paid,
                    "picture_url": User.query.filter_by(email=booking.email)
                    .first()
                    .google_picture_url
                    if len(User.query.filter_by(email=booking.email).all()) != 0
                    else "",
                    "time_created": str(booking.time_created),
                    "time_updated": str(booking.time_updated),
                }
                for booking in console_bookings
            ],
            "num_seats": NUM_SEATS,
            "num_console_seats": NUM_CONSOLE_SEATS,
        }
    )


@booking_blueprint.route("/<id>", methods=["PUT", "DELETE"])
@google_logged_in
@user_registered
@is_admin
def modify(id):
    json = request.json

    seat_type = json["seat_type"] if "seat_type" in json else None

    if request.method == "DELETE":
        booking = None
        booking = (
            Booking.query.get(id)
            if seat_type == "standard"
            else (
                ConsoleBooking.query.get(id)
                if seat_type == "console"
                else abort(400, "Invalid seat_type")
            )
        )

        if not booking:
            abort(404, "Booking does not exist")

        db.session.delete(booking)
        db.session.commit()

        return base_req()

    if request.method == "PUT":
        paid = json["paid"] if "paid" in json else None
        seat = json["seat"] if "seat" in json else None
        name = json["name"] if "name" in json else None
        email = json["email"] if "email" in json else None
        school_class = json["school_class"].upper() if "school_class" in json else None

        booking = None

        booking = (
            Booking.query.get(id)
            if seat_type == "standard"
            else (
                ConsoleBooking.query.get(id)
                if seat_type == "console"
                else abort(400, "Invalid seat_type")
            )
        )

        if not booking:
            abort(404, "Booking does not exist")

        booking.seat = seat if seat is not None else booking.seat
        booking.paid = paid if paid is not None else booking.paid
        booking.name = name if name is not None else booking.name
        booking.email = email if email is not None else booking.email
        booking.school_class = (
            school_class if school_class is not None else booking.school_class
        )

        db.session.commit()

        return base_req()


@booking_blueprint.route("/available")
@google_logged_in
@user_registered
def available():
    return base_req(
        response={
            "available_seats": [
                i for i in range(1, NUM_SEATS + 1) if not Booking.query.get(i)
            ],
            "available_console_seats": [
                i
                for i in range(1, NUM_CONSOLE_SEATS + 1)
                if not ConsoleBooking.query.get(i)
            ],
        }
    )


@booking_blueprint.route("/book", methods=["POST"])
@google_logged_in
@user_registered
def book():
    seat = request.json["seat"]
    seat_type = request.json["seat_type"]

    # Validate user input, must be an integer
    if not is_integer(seat):
        abort(400, "Seat must be integer")

    # Seat integer must be within bookable range
    seat_max = (
        NUM_SEATS
        if seat_type == "standard"
        else (
            NUM_CONSOLE_SEATS
            if seat_type == "console"
            else abort(400, "Invalid seat_type")  # only two types of seat
        )
    )

    if int(seat) < 1 or int(seat) > seat_max:
        abort(400, f"Seat must be in range 1 - {seat_max}")

    # Check if this seat is already booked by querying the database

    if (
        Booking.query.get(int(seat))
        if seat_type == "standard"
        else (
            ConsoleBooking.query.get(int(seat))
            if seat_type == "console"
            else abort(400, "Invalid seat_type")
        )
    ):
        abort(400, "Seat already booked.")

    # Check if this user already has a booking
    if (
        len(
            (
                Booking.query.filter_by(email=session["google_email"]).all()
                if seat_type == "standard"
                else (
                    ConsoleBooking.query.filter_by(email=session["google_email"]).all()
                    if seat_type == "console"
                    else abort(400, "Invalid seat_type")
                    # bad seat_type would have triggered abort earlier but good practice to always handle bad data
                )
            )
        )
        != 0  # realized this is whole if-statement is quite unreadable but it is very compact
    ):
        abort(
            400,
            "You have already booked a seat. Contact administrator for help with cancellation or seat movement.",
        )

    # Retrieve current user object
    user = User.query.filter_by(email=session["google_email"]).one()

    # Create new booking object
    booking = (
        Booking(
            seat=int(seat),
            name=session["google_name"],
            email=session["google_email"],
            school_class=user.school_class,
            paid=False,
        )
        if seat_type == "standard"
        else (
            ConsoleBooking(
                seat=int(seat),
                name=session["google_name"],
                email=session["google_email"],
                school_class=user.school_class,
                paid=False,
            )
            if seat_type == "console"
            else abort(400, "Invalid seat_type")
        )
    )

    # Add to database
    db.session.add(booking)
    db.session.commit()

    return base_req()


@booking_blueprint.route("/swish/<seat_type>/<id>")
@google_logged_in
@user_registered
def swish(seat_type, id):
    if not is_integer(id):
        abort(400, "Id must be integer")

    booking = (
        Booking.query.get(int(id))
        if seat_type == "standard"
        else (
            ConsoleBooking.query.get(int(id))
            if seat_type == "console"
            else abort(400, "Invalid seat_type")
        )
    )

    if not booking:
        abort(404, "Booking does not exist")

    generate_swish_qr(
        booking.name,
        booking.school_class,
        booking.seat,
        0 if seat_type == "standard" else 1,
    )
    return send_file("static/temp_swish.png", mimetype="image/png")
