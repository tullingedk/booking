###########################################################################
#                                                                         #
# tullingedk/booking                                                      #
# Copyright (C) 2018 - 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                         #
# Licensed under the terms of the GNU GPL-3.0 license, see LICENSE.       #
# https://github.com/tullingedk/booking                                   #
#                                                                         #
###########################################################################

from functools import wraps
from flask import session, abort

from models import User


def google_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "google_login" not in session:
            abort(401, "User is not authenticated using Google.")
        return f(*args, **kwargs)

    return decorated_function


def user_registered(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            user = User.query.filter_by(email=session["google_email"]).one()
        except Exception:
            abort(401, "User not registered.")
        return f(*args, **kwargs)

    return decorated_function
