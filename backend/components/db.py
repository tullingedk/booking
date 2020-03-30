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

import json
import os.path

import mysql.connector
import pymysql

if os.path.exists("override.mysql.json"):
    with open("override.mysql.json", "r") as f:
        mysql_config = json.load(f)
else:
    with open("mysql.json", "r") as f:
        mysql_config = json.load(f)


def dbConnection():
    try:
        cnx = mysql.connector.connect(
            user=mysql_config["username"],
            password=mysql_config["password"],
            host=mysql_config["host"],
            database=mysql_config["database"],
        )
    except mysql.connector.Error as err:
        print(err)
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


def pymysql_create_conn():
    """
    Creates a connection from config
    """
    return pymysql.connect(
        host=mysql_config["host"],
        user=mysql_config["username"],
        password=mysql_config["password"],
        db=mysql_config["database"],
    )


def dict_sql_query(query, fetchone=False):
    """
    Performs specified SQL query in database, return data as dict
    
    Try to use this one as much as possible when querying for data.
    """

    conn = pymysql_create_conn()

    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query)
            result = cursor.fetchone() if fetchone else cursor.fetchall()

        conn.commit()
    finally:
        conn.close()

    return result
