# next-release
* Use code formatter [prettier](https://prettier.io/) on frontend and admin.
* Use code formatter [black](https://github.com/psf/black) on backend.

# v2.0.1 (released on 2019-11-29)
* Solve issue [#3](https://github.com/VilhelmPrytz/datorklubben-booking/issues/3) - passwords cannot be longer than 50 characters. Length has been limited to 200 characters.
* Solve issue [#4](https://github.com/VilhelmPrytz/datorklubben-booking/issues/4) - admin area redirects to normal user interface

# v2.0.0 (released on 2019-11-29)
* Major re-work
* Split project into three (backend, frontend, admin)
* Backend now only returns JSON responses
* Frontend has been rewritten in React
* Admin area has been split into a separate React application to be served under a different route

# v1.0.0 (released on 2019-11-28, commit from 2019-11-13)
* Inital release