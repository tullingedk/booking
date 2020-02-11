#!/usr/bin/env python3

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

from datetime import datetime, timedelta

from components.db import sql_query
from components.tools import random_string


def validate_session(token):
    sessions = sql_query("SELECT * FROM sessions")
    now = datetime.now()

    for session in sessions:
        if token == session[0]:
            if session[1] > now:
                return True
            else:
                return False

    return False


def get_session(token):
    session = sql_query(f"SELECT * FROM sessions WHERE token='{token}'")

    if len(session) != 0:
        return session[0]

    return False


def new_session(remote_ip, is_admin=False):
    new_token = random_string(length=255)
    new_expire_date = datetime.now() + timedelta(hours=24)

    sql_query(
        f'INSERT INTO sessions (token, expire, ip, is_admin) VALUES ("{new_token}", "{new_expire_date}", "{remote_ip}", {is_admin})'
    )

    return new_token


def destroy_session(token):
    try:
        sql_query(f'DELETE FROM sessions WHERE token="{token}"')
    except Exception:
        return False

    return True


def clear_old_sessions():
    sessions = sql_query("SELECT * FROM sessions")
    now = datetime.now()

    for session in sessions:
        if session[1] < now:
            sql_query('DELETE FROM sessions WHERE token="{}"'.format(str(session[0])))
