FROM python:3.8-slim-buster

WORKDIR /var/www/app

# environment variables (TBD)

# create .venv dir (this is will pipenv will install)
RUN mkdir .venv

# install dep
RUN pip install --upgrade pip
RUN pip install pipenv

COPY . /var/www/app

RUN pipenv install --deploy

EXPOSE 5000
CMD [ "/var/www/app/entrypoint.sh" ]
