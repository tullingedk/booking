###########################################################################
#                                                                         #
# tullingedk/booking                                                      #
# Copyright (C) 2018 - 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                         #
# Licensed under the terms of the GNU GPL-3.0 license, see LICENSE.       #
# https://github.com/tullingedk/booking                                   #
#                                                                         #
###########################################################################

from flask import jsonify


def base_req(status=True, http_code=200, message="success", response={}):
    return (
        jsonify(
            {
                "status": status,
                "http_code": http_code,
                "message": message,
                "response": response,
            }
        ),
        http_code,
    )
