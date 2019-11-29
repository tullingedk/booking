#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
# Copyright (C) 2018 - 2019, Vilhelm Prytz <vilhelm@prytznet.se>                                             #
#                                                                                                            #
# This project is closed source. Allowed usage only covers the computer club on Tullinge gymnasium, Sweden.  #
# https://github.com/VilhelmPrytz/datorklubben-booking                                                       #
#                                                                                                            #
##############################################################################################################

# init database

from db import sql_query

# firstname
# lastname
# school_class
# email
# seat
# status
#       1: booked and paid
#       0: booked, not paid

def createDb():
    try:
        sql_query("""CREATE TABLE bookings (
name VARCHAR(255),
school_class VARCHAR(255),
email VARCHAR(255),
seat int NOT NULL,
status int NOT NULL,
date DATETIME,
ip VARCHAR(255),
PRIMARY KEY (seat)
);""")
    except Exception:
        print("bookings already exists")

def bc_createDb():
    try:
        sql_query("""CREATE TABLE bc_bookings (
name VARCHAR(255),
school_class VARCHAR(255),
email VARCHAR(255),
seat int NOT NULL,
status int NOT NULL,
date DATETIME,
ip VARCHAR(255),
PRIMARY KEY (seat)
);""")
    except Exception:
        print("bc_bookings already exists")

def create_sessions():
    try:
        sql_query("""CREATE TABLE sessions (
token VARCHAR(255) NOT NULL,
expire DATETIME NOT NULL,
ip VARCHAR(255) NOT NULL,
is_admin BOOLEAN NOT NULL,
PRIMARY KEY (token)
);""")
    except Exception:
        print("sessions table already exists")

if __name__ == "__main__":
    createDb()
    bc_createDb()
    create_sessions()
