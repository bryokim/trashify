from flask import jsonify
from flask_cors import cross_origin

from uuid import UUID

from api.views.core import core_view
from api.models.user import User


@core_view.route("/users/<id>")
@cross_origin(supports_credentials=True)
def get_user_by_id(id):
    print(UUID(id))
    user = User.get(UUID(id)).run()

    print(user)
    if not user:
        response = jsonify({"error": {"detail": "No user found"}})
    else:
        response = jsonify({"id": user.id, "email": user.email})

    return response
