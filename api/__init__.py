# Flask App
from flask import Flask
from flask_cors import CORS

# Database
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bunnet import init_bunnet

from dotenv import load_dotenv, find_dotenv
from os import environ as env

# Local
from api.config import DevelopmentConfig


def init_env():
    env_file = find_dotenv()

    if env_file:
        load_dotenv()


def init_db():
    uri = env.get("DB_URI")

    if uri:
        client = MongoClient(uri, server_api=ServerApi("1"))
    else:
        client = MongoClient(host="localhost")

    init_bunnet(database=client.new, document_models=["api.models.user.User"])


def create_app():
    init_env()

    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)

    # Allow requests from the frontend. Requests and responses can pass
    # credentials.
    CORS(app, origins=["http://localhost:8080"], supports_credentials=True)

    # Initialize the monogodb database.
    init_db()

    from api.views.auth import auth_view
    from api.views.core import core_view

    app.register_blueprint(auth_view)
    app.register_blueprint(core_view)

    return app
