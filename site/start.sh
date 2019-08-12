#!/bin/bash

cd /var/www/booking.vilhelmprytz.se/deploy
/usr/bin/env gunicorn --workers=5 --bind 127.0.0.1:7500 app:app
