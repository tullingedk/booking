import csv

import sys
from pathlib import Path

# Add parent folder
sys.path.append(str(Path(__file__).parent.parent.absolute()))

from components.db import sql_query


with open("scripts/students.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for row in csv_reader:
        email = row[1]
        class_name = row[2]

        if email != "" and email.lower() != "none":
            sql_query(
                """INSERT INTO google_allowed_users (email, school_class) VALUES ("{}", "{}");""".format(
                    email.lower(), class_name
                )
            )
