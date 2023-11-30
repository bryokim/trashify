from flask import jsonify, request
from flask_cors import cross_origin

from api.auth import fief_api
from api.views.auth import auth_view
from api.models.user import UserHelper

user_helper = UserHelper()


@auth_view.route("/signup", methods=["POST"])
@cross_origin(supports_credentials=True)
def signup():
    data = request.get_json(silent=True)

    if data.get("email") is None or data.get("password") is None:
        return jsonify({"detail": "must provide email and password"}), 400

    if user_helper.get_user_by_email(email=data.get("email")):
        return jsonify({"detail": "Email already registered"}), 400

    status_code, body = fief_api.create_user(data)
    if status_code != 201:
        return body, status_code

    body["password"] = data.get("password")
    new_user = user_helper.insert_user(body)

    response = jsonify({"id": new_user.id, "email": new_user.email})

    return response
