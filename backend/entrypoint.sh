#!/bin/bash

IP_HOST_MACHINE=$(/sbin/ip route|awk '/default/ { print $3 }')
RANDOM_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)

if [[ "$MYSQL_HOST" == "host.machine" ]]; then
    export MYSQL_HOST="$IP_HOST_MACHINE"
fi

if [[ "$SECRET_KEY" == "random" ]]; then
    export SECRET_KEY="$RANDOM_KEY"
fi

.venv/bin/gunicorn --workers=4 --bind 0.0.0.0:"$PORT" app:app
