###########################################################################
#                                                                         #
# tullingedk/booking                                                      #
# Copyright (C) 2018 - 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                         #
# Licensed under the terms of the GNU GPL-3.0 license, see LICENSE.       #
# https://github.com/tullingedk/booking                                   #
#                                                                         #
###########################################################################

from os import environ

import qrcode
import qrcode.image.svg

# normal, bc
amount_types = ["150", "80"]

SWISH_PHONE = environ.get("SWISH_PHONE", None)


def generate_swish_qr(name, school_class, seat, booking_type):
    amount = amount_types[booking_type]

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    data = f"C{SWISH_PHONE};{str(amount)};{name.replace(' ', '+')}+{school_class}+{'plats+' + str(seat)};0"

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()

    img.save("static/temp_swish.png")
