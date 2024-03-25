import json
import requests

from decouple import config
from uuid import UUID

from fief_client import Fief
from fief_client.integrations.flask import FiefAuth, get_cookie

FIEF_BASE_URL = config("FIEF_BASE_URL")
FIEF_TENANT_ID = config("FIEF_TENANT_ID")
FIEF_API_KEY = config("FIEF_API_KEY")
FIEF_CLIENT_ID = config("FIEF_CLIENT_ID")  # use when instantiating Fief
FIEF_CLIENT_ID_UUID = config(
    "FIEF_CLIENT_ID_UUID"
)  # use when calling the ADMIN API.
FIEF_CLIENT_SECRET = config("FIEF_CLIENT_SECRET")
FIEF_ADMIN_API_BASE_URL = config("FIEF_ADMIN_API_BASE_URL")
SESSION_COOKIE_NAME = config("SESSION_COOKIE_NAME")


class FiefAPI:
    def create_user(self, data: dict) -> tuple[int, dict]:
        res = requests.post(
            f"{FIEF_ADMIN_API_BASE_URL}/users",
            data=json.dumps(
                {
                    "email": data.get("email"),
                    "password": data.get("password"),
                    "email_verified": False,
                    "tenant_id": FIEF_TENANT_ID,
                }
            ),
            headers={
                "Authorization": f"Bearer {FIEF_API_KEY}",
                "Content-Type": "application/json",
            },
        )

        return res.status_code, res.json()

    def get_access_token(self, email: str, id: UUID) -> tuple[int, dict]:
        res = requests.post(
            f"{FIEF_ADMIN_API_BASE_URL}/users/{id}/access-token",
            data=json.dumps(
                {
                    "email": email,
                    "client_id": FIEF_CLIENT_ID_UUID,
                    "scopes": ["openid"],
                }
            ),
            headers={
                "Authorization": f"Bearer {FIEF_API_KEY}",
                "Content-Type": "application/json",
            },
        )

        return res.status_code, res.json()


fief_api = FiefAPI()

fief = Fief(
    FIEF_BASE_URL,
    FIEF_CLIENT_ID,
    FIEF_CLIENT_SECRET,
)

fief_auth = FiefAuth(fief, get_cookie(SESSION_COOKIE_NAME))
