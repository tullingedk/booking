##############################################################################################################
#   _____        _             _    _       _     _                  ____              _    _                #
#  |  __ \      | |           | |  | |     | |   | |                |  _ \            | |  (_)               #
#  | |  | | __ _| |_ ___  _ __| | _| |_   _| |__ | |__   ___ _ __   | |_) | ___   ___ | | ___ _ __   __ _    #
#  | |  | |/ _` | __/ _ \| '__| |/ / | | | | '_ \| '_ \ / _ \ '_ \  |  _ < / _ \ / _ \| |/ / | '_ \ / _` |   #
#  | |__| | (_| | || (_) | |  |   <| | |_| | |_) | |_) |  __/ | | | | |_) | (_) | (_) |   <| | | | | (_| |   #
#  |_____/ \__,_|\__\___/|_|  |_|\_\_|\__,_|_.__/|_.__/ \___|_| |_| |____/ \___/ \___/|_|\_\_|_| |_|\__, |   #
#                                                                                                    __/ |   #
#                                                                                                   |___/    #
#                                                                                                            #
# Copyright (C) 2018 - 2020, Vilhelm Prytz <vilhelm@prytznet.se>                                             #
#                                                                                                            #
# This project is closed source. Allowed usage only covers the computer club on Tullinge gymnasium, Sweden.  #
# https://github.com/VilhelmPrytz/datorklubben-booking                                                       #
#                                                                                                            #
##############################################################################################################

# imports
from flask import jsonify

from google.oauth2 import id_token
from google.auth.transport import requests

import requests as requests_module

from components.configuration import read_config

config = read_config()

GOOGLE_CLIENT_ID = config["google_clientid"]


def google_login(token, hd_name):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), GOOGLE_CLIENT_ID
        )

        # check for valid iss
        if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            return {
                "status": False,
                "resp": (
                    jsonify(
                        {
                            "status": False,
                            "http_code": 400,
                            "message": "Invalid issuer.",
                            "response": {},
                        }
                    ),
                    400,
                ),
            }

        # if auth request is from a G Suite domain:
        if hd_name and "hd" not in idinfo:
            return {
                "status": False,
                "resp": (
                    jsonify(
                        {
                            "status": False,
                            "http_code": 400,
                            "message": "User is not using hosted email, please use your school address.",
                            "response": {},
                        }
                    ),
                    400,
                ),
            }

        if hd_name and idinfo["hd"] != hd_name:
            return {
                "status": False,
                "resp": (
                    jsonify(
                        {
                            "status": False,
                            "http_code": 400,
                            "message": "Wrong hosted domain, please use your school address.",
                            "response": {},
                        }
                    ),
                    400,
                ),
            }

    except ValueError:
        # Invalid token
        return {
            "status": False,
            "resp": (
                jsonify(
                    {
                        "status": False,
                        "http_code": 400,
                        "message": "Invalid token.",
                        "response": {},
                    }
                ),
                400,
            ),
        }

    # user signed in
    r = requests_module.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")

    if r.status_code is not requests_module.codes.ok:
        return {
            "status": False,
            "resp": (
                jsonify(
                    {
                        "status": False,
                        "http_code": 500,
                        "message": "Could not verify token.",
                        "response": {},
                    }
                ),
                500,
            ),
        }

    data = r.json()

    # verify
    if data["aud"] != GOOGLE_CLIENT_ID:
        return {
            "status": False,
            "resp": (
                jsonify(
                    {
                        "status": False,
                        "http_code": 400,
                        "message": "'aud' is invalid!",
                        "response": {},
                    }
                ),
                400,
            ),
        }

    # if all good
    return {"status": True, "resp": {"data": data, "idinfo": idinfo,}}
