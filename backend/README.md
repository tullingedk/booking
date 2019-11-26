# datorklubben-booking/backend

Backend written in Python 3, Flask.

## Routes

### Entrypoint
* `/backend/info` - returns general system information
* `/backend/auth` - authentication, used for creating user sessions
* `/backend/validate_session` - validate user token to see if valid or expired

### Bookings
* `/backend/bookings` - returns list of all bookings with all information
* `/backend/bookings/<id>` - returns information about specific booking
* `/backend/book` - creating new booking in system

### Board and console bookings
* `/backend/bc/bookings` - returns list of all bc_bookings with all information
* `/backend/bc/bookings/<id>` - returns information about specific bc_booking
* `/backend/bc/book` - create new bc_booking in system

