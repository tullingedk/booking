###########################################################################
#                                                                         #
# tullingedk/booking                                                      #
# Copyright (C) 2018 - 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                         #
# Licensed under the terms of the GNU GPL-3.0 license, see LICENSE.       #
# https://github.com/tullingedk/booking                                   #
#                                                                         #
###########################################################################

from flask import Blueprint, request, abort, session, redirect

from base import base_req
from decorators.auth import google_logged_in, user_registered
from models import db, User
from validation import input_validation, length_validation

from os import environ
from oauthlib.oauth2 import WebApplicationClient
from requests import get, post
from json import dumps

# define configuration (from environment variables)
GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_HOSTED_DOMAIN = environ.get("GOOGLE_HOSTED_DOMAIN", None)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
FRONTEND_URL = environ.get("FRONTEND_URL", None)
REGISTER_PASSWORD = environ.get("REGISTER_PASSWORD", None)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

auth_blueprint = Blueprint("auth", __name__, template_folder="../templates")

# functions
def get_google_provider_cfg():
    return get(GOOGLE_DISCOVERY_URL).json()


@auth_blueprint.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )

    return base_req(response={"login_url": request_uri})


@auth_blueprint.route("/login/callback")
def callback():
    # Get authorization code Google sent back
    code = request.args.get("code")

    # If no code was sent
    if not code:
        abort(400, "missing oauth token")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens
    client.parse_request_body_response(dumps(token_response.json()))

    # Now that you have tokens let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        if "hd" not in userinfo_response.json():
            abort(
                401,
                "Email is not hosted domain. Please use organization Google Account.",
            )

        hd = userinfo_response.json()["hd"]

        if hd != GOOGLE_HOSTED_DOMAIN:
            abort(
                401,
                f"Booking system only allows hosted domains for organization {GOOGLE_HOSTED_DOMAIN}. Your organization, {hd}, is not allowed.",
            )

        session["google_login"] = True
        session["google_unique_id"] = userinfo_response.json()["sub"]
        session["google_email"] = userinfo_response.json()["email"]
        session["google_picture_url"] = userinfo_response.json()["picture"]
        session["google_name"] = userinfo_response.json()["name"]

        return redirect(FRONTEND_URL)

    abort(400, "User email not available or not verified by Google")


@auth_blueprint.route("/validate")
@google_logged_in
@user_registered
def validate():
    return base_req(message="User valid.")


@auth_blueprint.route("/register", methods=["POST"])
@google_logged_in
def register():
    user = User.query.filter_by(email=session["google_email"])

    if user:
        abort(400, "User already registered.")

    password = request.json["password"]
    school_class = request.json["school_class"]

    if password != REGISTER_PASSWORD:
        abort(401, "Invalid password")

    if input_validation(school_class) and length_validation(
        school_class, 4, 6, vanity="School class"
    ):
        user = User(email=session["google_email"], school_class=school_class)

        db.session.add(user)
        db.session.commit()

        return base_req(message="user registered")

    abort(500)
