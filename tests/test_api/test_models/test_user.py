from api.models.user import User

from bcrypt import hashpw, gensalt
from datetime import datetime


def test_user():
    user_data = {
        "email": "test@test.com",
        "hashed_password": hashpw("password".encode(), gensalt()),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "email_verified": False,
    }

    new_user = User(**user_data)

    print(new_user)
    assert new_user


if __name__ == "__main__":
    test_user()
