FROM nikolaik/python-nodejs:python3.9-nodejs14

WORKDIR /var/www/app

# environment variables (TBD)

# create .venv dir (this is where pipenv will install)
RUN mkdir .venv

# install dep
RUN apt-get update && apt-get install iproute2 -y

COPY . /var/www/app

# backend
WORKDIR /var/www/app/backend
RUN pipenv install --deploy

# frontend
WORKDIR /var/www/app/frontend
RUN export REACT_APP_BACKEND_URL="/" && npm run build

WORKDIR /var/www/app

EXPOSE 5000
CMD [ "/var/www/app/entrypoint.sh" ]
