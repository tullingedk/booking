# datorklubben-booking

Booking system for Tullinge gymnasium datorklubb. Initial revision was coded during 2018, major overhaul in 2019 (split application into three).

Production application is available at [booking.vilhelmprytz.se](https://booking.vilhelmprytz.se).

## Backend

The backend is coded in Python 3 Flask. It's meant to be served under the `/backend` route. Install the required modules in `backend/requirements.txt` using `pip3` and update configuration values in `config.json` and `mysql.json` (if developing, you can use `override.config.json` and `override.mysql.json` to avoid configuration being commited to project).

The backend also requires a `redis` server for rate limiting cache.

Recommendation: use `supervisor` and `gunicorn` in conjunction with `nginx` `proxy_pass` in order to serve the backend application.

## Frontend

The frontend is coded in React. It's mean to be served under the project root, `/`. Replace the configuration value found in `src/global_variables.js` in order to match your setup. You can build the project using `npm run build`. Serve using `nginx`.

## Admin

The admin frontend is coded in React. It's meant to be served un the `/admin` route. Replace the configuration value found in `src/global_variables.js` in order to match your setup. You can build the project using `npm run build`. Serve using `nginx`. Uses same backend as the public frontend.

## File structure

* `backend`, application route `/backend` - Python 3 Flask backend application
* `frontend`, application route `/` - React application, frontend
* `admin`, application route `/admin` - React application, frontend
