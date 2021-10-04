###########################################################################
#                                                                         #
# tullingedk/booking                                                      #
# Copyright (C) 2018 - 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                         #
# Licensed under the terms of the GNU GPL-3.0 license, see LICENSE.       #
# https://github.com/tullingedk/booking                                   #
#                                                                         #
###########################################################################

from flask import Blueprint, request, abort

from dataclasses import asdict

from decorators.auth import google_logged_in, user_registered, is_admin
from models import db, Admin, User
from base import base_req
from validation import input_validation, length_validation

admin_blueprint = Blueprint("admin", __name__, template_folder="../templates")


@admin_blueprint.route("/admin", methods=["POST", "GET", "DELETE"])
@google_logged_in
@user_registered
@is_admin
def admin():
    if request.method == "GET":
        return base_req(response=[asdict(admin) for admin in Admin.query.all()])

    if request.method == "POST":
        if "email" not in request.json:
            abort(400, "Missing key email")

        admin = Admin(email=request.json["email"])

        db.session.add(admin)
        db.session.commit()

        return base_req()

    if request.method == "DELETE":
        if "email" not in request.json:
            abort(400, "Missing key email")

        search = Admin.query.filter_by(email=request.json["email"]).all()

        if not search:
            abort(404, "Admin with specified email does not exist")

        db.session.delete(Admin.query.filter_by(email=request.json["email"]).one())
        db.session.commit()

        return base_req()


@admin_blueprint.route("/user", methods=["POST", "GET", "DELETE"])
@google_logged_in
@user_registered
@is_admin
def user():
    if request.method == "GET":
        return base_req(response=[asdict(user) for user in User.query.all()])

    if request.method == "POST":
        if "email" not in request.json:
            abort(400, "Missing key email")

        if "school_class" not in request.json:
            abort(400, "Missing key school_class")

        email = request.json["email"]
        school_class = request.json["school_class"].upper()

        user = User.query.filter_by(email=email).all()

        if len(user) > 0:
            abort(400, "User already registered.")

        if input_validation(school_class) and length_validation(
            school_class, 4, 6, vanity="School class"
        ):
            user = User(email=email, school_class=school_class)

            db.session.add(user)
            db.session.commit()

            return base_req(
                message="user registered",
                response={
                    "email": email,
                    "school_class": school_class,
                },
            )

        abort(500)

    abort(501, f"{request.method} on this method not yet supported")
