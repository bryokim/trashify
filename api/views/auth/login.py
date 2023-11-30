from flask import jsonify, request
from flask_cors import cross_origin
from os import environ as env

from api.auth import fief_api
from api.views.auth import auth_view
from api.models.user import UserHelper

user_helper = UserHelper()

SESSION_COOKIE_NAME = env.get("SESSION_COOKIE_NAME")


@auth_view.route("/this-user")
@cross_origin(supports_credentials=True)
def this_user():
    print(request.cookies.get("trashify_user_session"))

    return jsonify({"this_user": "OK"})


@auth_view.route("/login", methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    data = request.get_json(silent=True)

    if data.get("email") is None or data.get("password") is None:
        return jsonify({"detail": "Must provide email and password"}), 400

    user = user_helper.get_user_by_email(data.get("email"))

    if not user:
        return jsonify({"detail": "Invalid email or password"}), 400

    if not user_helper.verify_password(
        data.get("password"), user.hashed_password
    ):
        return jsonify({"detail": "Invalid email or password"}), 400

    status_code, access_token_info = fief_api.get_access_token(
        user.email, user.id
    )

    if status_code != 200:
        return access_token_info, status_code

    response = jsonify({"id": user.id, "email": user.email})

    response.set_cookie(
        SESSION_COOKIE_NAME,
        access_token_info["access_token"],
        max_age=access_token_info["expires_in"],
    )

    return response
