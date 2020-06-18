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
from models import db, Admin
from base import base_req

admin_blueprint = Blueprint("admin", __name__, template_folder="../templates")


@admin_blueprint.route("/user", methods=["POST", "GET", "DELETE"])
@google_logged_in
@user_registered
@is_admin
def user():
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
