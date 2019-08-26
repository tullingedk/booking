#!/usr/bin/env python
# simple script for removing tables

from db import sql_query

sql_query("DROP TABLE bookings")
sql_query("DROP TABLE bc_bookings")
