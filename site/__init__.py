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
    sql_query("""CREATE TABLE bookings (
firstname VARCHAR(255),
lastname VARCHAR(255),
school_class VARCHAR(255),
email VARCHAR(255),
seat int NOT NULL,
status int NOT NULL,
date DATETIME,
PRIMARY KEY (seat)
);""")

def bc_createDb():
    sql_query("""CREATE TABLE bc_bookings (
firstname VARCHAR(255),
lastname VARCHAR(255),
school_class VARCHAR(255),
email VARCHAR(255),
seat int NOT NULL,
status int NOT NULL,
date DATETIME,
PRIMARY KEY (seat)
);""")

if __name__ == "__main__":
    createDb()
