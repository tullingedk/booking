# datorklubben-booking/backend

Backend written in Python 3, Flask.

## Configuration

Update `config.json` and `mysql.json` with appropriate values. Passwords should be between 3 and 200 characters long.

## Requirements

The backend requires a `redis` server running (for rate limiting cache). You can specify connection details in `config.json`.

## Routes

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
