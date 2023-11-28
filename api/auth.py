import json
import requests

from decouple import config
from uuid import UUID

TENANT_ID = config("FIEF_TENANT_ID")
FIEF_API_KEY = config("FIEF_API_KEY")
FIEF_CLIENT_ID = config("FIEF_CLIENT_ID")
FIEF_ADMIN_API_BASE_URL = config("FIEF_ADMIN_API_BASE_URL")


class FiefAPI:
    def create_user(self, data: dict) -> tuple[int, dict]:
        res = requests.post(
            f"{FIEF_ADMIN_API_BASE_URL}/users",
            data=json.dumps(
                {
                    "email": data.get("email"),
                    "password": data.get("password"),
                    "email_verified": False,
                    "tenant_id": TENANT_ID,
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
                    "client_id": FIEF_CLIENT_ID,
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
