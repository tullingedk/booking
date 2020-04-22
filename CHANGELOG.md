# Changelog

## next-release

* Update dependencies

## v2.5.0 (released on 2020-04-19)

* Use `config.json` and don't hardcode all values (swish number, swish name, Google Client ID etc.)
* Update dependencies

## v2.4.2 (released on 2020-04-11)

* Update FQDN.
* Add LICENSE file.
* Update dependencies

## v2.4.1 (relesed on 2020-03-31)

* Fix [#8](https://github.com/VilhelmPrytz/datorklubben-booking/issues/8) - Use Google Sign-In for authentication
* Update dependencies

## v2.3.1 (released on 2020-03-11)

* Fix [#9](https://github.com/VilhelmPrytz/datorklubben-booking/issues/9) - tooltips now hide when opening the seat modal
* Decapitalize BankID name
* Make it more clear to users what user data the application stores and for what purposes.
* Update dependencies

## v2.3.0 (released on 2020-02-27)

* Updated copyright years
* Move backend scripts to `backend/scripts` directory
* Update dependencies
* Fix [#12](https://github.com/VilhelmPrytz/datorklubben-booking/issues/12) - show number of available "bc" seats

## v2.2.0 (released on 2020-02-08)

* Fix [#10](https://github.com/VilhelmPrytz/datorklubben-booking/issues/10) - misspelling on "brädspelsplatser"
* Environment variable `DEVELOPMENT` removes CORS-policy on `backend`
* Add konami-code easteregg on frontend

## v2.1.2 (released on 2020-02-07)

* Update Bootstrap version (from `4.3.1` to `4.4.1`).
* Use pipenv for backend
* Update dependencies

## v2.1.1 (released on 2020-01-22)

* Improve `Access-Control-Allow-Origin` header policy on backend.

## v2.1.0 (released on 2019-12-08)

* Solve issue [#6](https://github.com/VilhelmPrytz/datorklubben-booking/issues/6) - admin/frontend: optimize for mobile usage
* Solve issue [#5](https://github.com/VilhelmPrytz/datorklubben-booking/issues/5) - backend: rate limit API calls, backend now requires `redis` in order to run
* Update dependencies (housekeeping)
* Add GitHub workflow (test backend application using `flake8` and `black`).
* Solve issue [#7](https://github.com/VilhelmPrytz/datorklubben-booking/issues/7) - backend: re-organize and re-structure (refactoring), move routes into separate blueprints
* Add `docker-compose` configuration for development.
* Use code formatter [prettier](https://prettier.io/) on frontend and admin.
* Use code formatter [black](https://github.com/psf/black) on backend.

## v2.0.1 (released on 2019-11-29)

* Solve issue [#3](https://github.com/VilhelmPrytz/datorklubben-booking/issues/3) - passwords cannot be longer than 50 characters. Length has been limited to 200 characters.
* Solve issue [#4](https://github.com/VilhelmPrytz/datorklubben-booking/issues/4) - admin area redirects to normal user interface

## v2.0.0 (released on 2019-11-29)

* Major rework
* Split project into three (backend, frontend, admin)
* Backend now only returns JSON responses
* Frontend has been rewritten in React
* Admin area has been split into a separate React application to be served under a different route

## v1.0.0 (released on 2019-11-28, commit from 2019-11-13)

* Initial release
