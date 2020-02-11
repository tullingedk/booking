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

from components.db import sql_query

NUM_TOTAL_BC_SEATS = 10


def get_bc_bookings():
    """Returns list of all bc_bookings"""

    return sql_query("SELECT * FROM bc_bookings")


def bc_get_available_seats_list():
    """Returns list of available bc_booking seats"""

    bookings = get_bc_bookings()
    available_seats = list(range(1, NUM_TOTAL_BC_SEATS + 1))

    if bookings:
        for booking in bookings:
            for seat in range(1, NUM_TOTAL_BC_SEATS + 1):
                if seat == int(booking[3]):
                    available_seats.remove(seat)

    return available_seats


def get_specific_bc_booking_details(id):
    """Returns list variable with bc_booking details of specified id"""

    allBookings = get_bc_bookings()

    for booking in allBookings:
        if int(id) == int(booking[3]):
            return booking
