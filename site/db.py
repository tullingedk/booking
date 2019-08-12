# Datorklubben Booking sytsem
# db file
# (c) Vilhelm Prytz 2019
# https://www.vilhelmprytz.se

import mysql.connector

import json
with open("mysql.json", "r") as f:
    mysql_config = json.load(f)

def dbConnection():
    try:
        cnx = mysql.connector.connect(user=mysql_config["username"], password=mysql_config["password"],
                              host=mysql_config["host"],
                              database=mysql_config["database"])
    except mysql.connector.Error as err:
        print("error")
        quit(1)

    cursor = cnx.cursor()
    return cnx, cursor


def sql_query(query):
    cnx, cursor = dbConnection()

    cursor.execute(query)

    try:
        result = cursor.fetchall()
    except Exception:
        result = None

    cnx.commit()
    cursor.close()
    cnx.cursor()

    return result
