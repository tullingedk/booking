###########################################################################
#                                                                         #
# tullingedk/booking                                                      #
# Copyright (C) 2018 - 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                         #
# Licensed under the terms of the GNU GPL-3.0 license, see LICENSE.       #
# https://github.com/tullingedk/booking                                   #
#                                                                         #
###########################################################################

from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


@dataclass
class User(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    email: str = db.Column(db.String(255), unique=True, nullable=False)
    school_class: str = db.Column(db.String(255), unique=False, nullable=False)

    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())


@dataclass
class Admin(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    email: str = db.Column(db.String(255), unique=True, nullable=False)

    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())


@dataclass
class Booking(db.Model):
    seat: int = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name: str = db.Column(db.String(255), unique=False, nullable=False)
    email: str = db.Column(db.String(255), unique=True, nullable=False)
    school_class: str = db.Column(db.String(15), unique=False, nullable=False)
    paid: bool = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
