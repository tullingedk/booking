# datorklubben-booking/backend

Backend API written in Flask.

## Configuration

Update `config.json` and `mysql.json` with appropriate values. Passwords should be between 3 and 200 characters long.

## Requirements

Requires Python 3.6 or newer (recommended 3.7/3.8).

The backend requires a `redis` server running (for rate limiting cache). You can specify connection details in `config.json`.

## Working locally

This project uses Pipenv. Make sure you're in the `backend` folder.

Start temporary MySQL and Redis containers.

```bash
docker-compose up -d
```

Install dependencies.

```bash
pipenv install --dev
```

Enter shell of environment.

```bash
pipenv shell
```

Run app.

```bash
python app.py
```

Define the `DEVELOPMENT` variable to disable the CORS-policy while working locally (you can create `backend/.env` and define it there before using `pipenv shell`).

## Routes

These are routes the API exposes.

### Entrypoint

* `/backend/info` - returns general system information
* `/backend/auth` - authentication, used for creating user sessions
* `/backend/validate_session` - validate user token to see if valid or expired
* `/backend/logout` - destroy user session

### Bookings

* `/backend/bookings` - returns list of all bookings with all information
* `/backend/book` - creating new booking in system
* `/backend/swish/<qr>` - PNG Swish QR
* `/backend/available_seat_list` - returns list of seats available to book by users

### Board and console bookings

* `/backend/bc/bookings` - returns list of all bc_bookings with all information
* `/backend/bc/book` - create new bc_booking in system
* `/backend/bc/swish/<qr>` - PNG Swish QR
* `/backend/bc/available_seat_list` - returns list of seats available to book by users

### Admin

* `/backend/admin/auth` - authentication, used for creating admin sessions
* `/backend/admin/paid/<id>` - mark booking as paid
* `/backend/admin/unpaid/<id>` - mark booking as unpaid
* `/backend/admin/bc/paid/<id>` - mark bc booking as paid
* `/backend/admin/bc/unpaid/<id>` - mark bc booking as unpaid
