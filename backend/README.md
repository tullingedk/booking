# tullingedk/booking/backend

Flask backend.

## Environment Variables

* `GOOGLE_CLIENT_ID` - Client ID for Google Sign-In
* `GOOGLE_CLIENT_SECRET` - Client secret for Google Sign-In
* `GOOGLE_HOSTED_DOMAIN` - G Suite hosted domain to limit logins to
* `BACKEND_URL` - URL for the backend, i.e. `https://booking.tgdk.se`.
* `FRONTEND_URL` - URL for the frontend, i.e. `https://booking.tgdk.se` (yes this can be the same as backend URL).
* `MYSQL_USER` - MySQL username used for database connections.
* `MYSQL_PASSWORD` - MySQL password used for database connections.
* `MYSQL_HOST` - MySQL hostname used for database connections.
* `MYSQL_DATABASE` - MySQL database name used for database connections.
* `REGISTER_PASSWORD` - Password for user registration.
* `SWISH_PHONE` - Phone number displayed as payment recipient. Format `+46XXXXXXXXX`
* `SECRET_KEY` - Used by Flask for sessions. Can be regenerated without dataloss. Does not have to be defined in development.

### Optional (development)

* `OAUTHLIB_INSECURE_TRANSPORT` - Set to `1` during development to allow for HTTP auth.
* `DEVELOPMENT` - Define to enable lazy CORS policy.
