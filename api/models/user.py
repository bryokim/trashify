from bunnet import Document, Link
from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import Literal
from uuid import UUID, uuid4
from bcrypt import hashpw, gensalt, checkpw

from api.models.collector import Collector


class Schedule(BaseModel):
    interval: Literal["weekly", "fortnightly", "triweekly", "monthly"]
    start_date: date
    days_of_week: list[str]


class Location(BaseModel):
    state: str
    city: str
    street: str | None = None
    estate: str | None = None
    house_no: str | None = None
    country: str = "KE"


class User(Document):
    id: UUID = Field(default_factory=uuid4)
    email: str
    hashed_password: bytes
    username: str | None = None
    phone_number: str | None = None

    created_at: datetime
    updated_at: datetime
    email_verified: bool

    location: Location | None = None
    schedule: Schedule | None = None

    collector: Link[Collector] | None = None

    class Settings:
        name = "users"
        use_state_management = True


class UserHelper:
    def insert_user(self, user_data: dict) -> User:
        new_user = User(
            id=user_data["id"],
            email=user_data["email"],
            created_at=user_data["created_at"],
            updated_at=user_data["updated_at"],
            email_verified=user_data["email_verified"],
            is_active=user_data["is_active"],
            hashed_password=hashpw(user_data["password"].encode(), gensalt()),
        )

        new_user.create()

        return new_user

    def get_user_by_email(self, email: str):
        return User.find_one({"email": email}).run()

    def verify_password(self, password: str, hashed_password: bytes):
        return checkpw(password.encode(), hashed_password)
