from flask import jsonify

from api.views.core import core_view


@core_view.route("/status")
def status():
    return jsonify({"status": "OK"})
