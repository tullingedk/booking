###########################################################################
#                                                                         #
# tullingedk/booking                                                      #
# Copyright (C) 2018 - 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                         #
# Licensed under the terms of the GNU GPL-3.0 license, see LICENSE.       #
# https://github.com/tullingedk/booking                                   #
#                                                                         #
###########################################################################

import sys
from pathlib import Path

# add parent folder
sys.path.append(str(Path(__file__).parent.parent.absolute()))

from app import db, app
from models import User

new_email = input("Enter email: ")
new_school_class = input("Enter school class: ")

user = User(email=new_email, school_class=new_school_class,)

with app.app_context():
    db.session.add(user)
    db.session.commit()
