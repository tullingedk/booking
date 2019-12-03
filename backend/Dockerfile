FROM alpine:latest

LABEL maintainer="vilhelm@prytznet.se"

RUN apk add --no-cache python3-dev build-base zlib-dev jpeg-dev \
    && pip3 install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt
RUN pip3 --no-cache-dir install gunicorn

EXPOSE 5000

ENTRYPOINT [ "gunicorn" ]
CMD ["--workers=5", "--bind", "0.0.0.0:5000", "app:app"]