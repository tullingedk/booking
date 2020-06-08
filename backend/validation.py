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

ILLEGAL_CHARACTERS = ["<", ">", ";"]
ALLOWED_CHARACTERS = list(printable) + ["å", "ä", "ö", "Å", "Ä", "Ö"]


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
