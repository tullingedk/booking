#!/bin/bash

docker build -t tullingedk/booking:latest backend
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin && docker push tullingedk/booking:latest
