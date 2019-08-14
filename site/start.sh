#!/bin/bash

cd /var/www/booking.vilhelmprytz.se/deploy
rm -rf /var/www/booking.vilhelmprytz.se/flask_session

/usr/bin/env gunicorn --workers=5 --bind 127.0.0.1:7500 app:app
