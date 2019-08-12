#!/usr/bin/python

from db import *

id = raw_input("Enter ID of seat that should be marked as paid: ")

sql_query("""UPDATE bookings SET status = 0 WHERE seat=""" + id)
