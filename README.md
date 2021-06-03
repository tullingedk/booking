# tullingedk/booking

Booking system for Tullinge gymnasium datorklubb. Initial revision was coded during 2018, major overhaul in 2019 (split application into three). Made open-source in 2020 and rewritten again.

Production application is available at [booking.tgdk.se](https://booking.tgdk.se).

## Backend

The backend is coded in Python 3 Flask. It's meant to be served under the `/api` route. You need to have Pipenv install to run it locally.

See `backend/README.md` for install instructions. You need to set environment variables. They can be set in `.env`.

For production, use the Docker image. There is a `prod.yml` docker-compose configuration.

```bash
docker-compose -f prod.yml up -d
```

## Frontend

The frontend is coded in React. It's mean to be served under the project root, `/`. Before you build, set the environment variable `REACT_APP_BACKEND_URL` to the URL of your backend (e.g. `https://booking.tgdk.se`).

Build the project.

```bash
npm run build
```

Serve the static files generated in `build`.

## File structure

- `backend`, application route `/backend` - Python 3 Flask backend application
- `frontend`, application route `/` - React application, frontend

## License

This project is licensed under the terms of the GNU General Public License 3.0. This license was added to the project in the commit [56df59a](https://github.com/tullingedk/booking/commit/56df59a5d90060c44f4d3f1570d2ac95705a9068). The author of all previous commits, Vilhelm Prytz, has decided to license all previous work and commits under the same license.

## Contributors ✨

Created, initially written and maintained by [Vilhelm Prytz](https://github.com/VilhelmPrytz).

Copyright (C) 2018 - 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al.
