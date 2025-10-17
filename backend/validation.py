###########################################################################
#                                                                         #
# tullingedk/booking                                                      #
# Copyright (C) 2018 - 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                         #
# Licensed under the terms of the GNU GPL-3.0 license, see LICENSE.       #
# https://github.com/tullingedk/booking                                   #
#                                                                         #
###########################################################################

from flask import abort
from string import printable
import re

ILLEGAL_CHARACTERS = ["<", ">", ";", "&", "|", "`", "$", "(", ")", "{", "}", "[", "]"]
ALLOWED_CHARACTERS = list(printable) + ["å", "ä", "ö", "Å", "Ä", "Ö"]

# Email validation regex (RFC 5322 simplified)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


def is_integer(i):
    try:
        int(i)
    except Exception:
        return False
    return True


def input_validation(i):
    if any(x in i for x in ILLEGAL_CHARACTERS):
        abort(
            400, "Input variable contains illegal characters (stick to the alphabet)."
        )

    if any(x not in ALLOWED_CHARACTERS for x in i):
        abort(
            400,
            "Input variable contains non-allowed characters (stick to the alphabet).",
        )

    return True


def length_validation(i, min, max, vanity=None):
    if len(i) < min:
        abort(
            400, f"{vanity} needs to be at least {min} characters long"
        ) if vanity else abort(400, f"Data too short (minimum {min})")

    if len(i) > max:
        abort(
            400, f"{vanity} cannot be longer than {max} characters"
        ) if vanity else abort(400, f"Data too long (max {max})")

    return True


def email_validation(email):
    """Validate email format"""
    if not email or not isinstance(email, str):
        abort(400, "Email must be a valid string")
    
    if len(email) > 500:
        abort(400, "Email address is too long (max 500 characters)")
    
    if not EMAIL_REGEX.match(email):
        abort(400, "Invalid email format. Please provide a valid email address.")
    
    return True
