###########################################################################
#                                                                         #
# tullingedk/booking                                                      #
# Copyright (C) 2018 - 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                         #
# Licensed under the terms of the GNU GPL-3.0 license, see LICENSE.       #
# https://github.com/tullingedk/booking                                   #
#                                                                         #
###########################################################################

from flask import session, abort, jsonify, Blueprint, request, send_file

from decorators.auth import google_logged_in, user_registered
from validation import input_validation, length_validation, is_integer
from models import db, Booking, User
from base import base_req
from swish import generate_swish_qr

booking_blueprint = Blueprint("booking", __name__, template_folder="../templates")

NUM_SEATS = 48


@booking_blueprint.route("/bookings")
@google_logged_in
@user_registered
def bookings():
    bookings = Booking.query.all()

    response = [
        {
            "seat": booking.seat,
            "name": booking.name,
            "school_class": booking.school_class,
            "paid": booking.paid,
            "time_created": booking.time_created,
            "time_updated": booking.time_updated,
        }
        for booking in bookings
    ]

    return base_req(response=response)


@booking_blueprint.route("/available")
@google_logged_in
@user_registered
def available():
    response = [i for i in range(1, NUM_SEATS + 1) if not Booking.query.get(i)]

    return base_req(response=response)


@booking_blueprint.route("/book", methods=["POST"])
@google_logged_in
@user_registered
def book():
    seat = request.json["seat"]

    # Validate user input, must be an integer
    if not is_integer(seat):
        abort(400, "Seat must be integer")

    # Seat integer must be within bookable range
    if int(seat) < 1 or int(seat) > NUM_SEATS:
        abort(400, f"Seat must be in range 1 - {NUM_SEATS}")

    # Check if this seat is already booked by querying the database
    if Booking.query.get(int(seat)):
        abort(400, f"Seat already booked.")

    # Check if this user already has a booking
    if len(Booking.query.filter_by(email=session["google_email"])) != 0:
        abort(
            400,
            "You have already booked a seat. Contact administrator for help with cancellation or seat movement.",
        )

    # Retrieve current user object
    user = User.query.filter_by(email=session["google_email"]).one()

    # Create new booking object
    booking = Booking(
        seat=int(seat),
        name=session["google_name"],
        email=session["google_email"],
        school_class=user.school_class,
        paid=False,
    )

    # Add to database
    db.session.add(booking)
    db.session.commit()

    return base_req()


@booking_blueprint.route("/swish/<id>")
@google_logged_in
@user_registered
def swish(id):
    if not is_integer(id):
        abort(400, "Id must be integer")

    booking = Booking.query.get(int(id))

    if not booking:
        abort(404, "Booking does not exist")

    generate_swish_qr(booking.name, booking.school_class, booking.seat, 0)
    return send_file("static/temp_swish.png", mimetype="image/png")
