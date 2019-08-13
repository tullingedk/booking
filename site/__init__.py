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
firstname VARCHAR(255),
lastname VARCHAR(255),
school_class VARCHAR(255),
email VARCHAR(255),
seat int NOT NULL,
status int NOT NULL,
date DATETIME,
PRIMARY KEY (seat)
);""")
    except Exception:
        print("bookings already exist")

def bc_createDb():
    try:
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
    except Exception:
        print("bc_bookings already exist")

if __name__ == "__main__":
    createDb()
    bc_createDb()
