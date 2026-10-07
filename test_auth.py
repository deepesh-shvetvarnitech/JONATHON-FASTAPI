import asyncio

from src.auth.service import UserService, pwd_context
from src.db.main import get_session


async def test_authenticate():
    user_service = UserService()

    async for session in get_session():

        user = await user_service.get_user_by_email(
            "hanuman@gmail.com",
            session,
        )

        if user is None:
            print("USER NOT FOUND")
            return

        print("USER FOUND")
        print("Username:", user.username)
        print("Email:", user.email)
        print("Password hash exists:", bool(user.password_hash))

        password_valid = pwd_context.verify(
            "password567",
            user.password_hash,
        )

        print("PASSWORD VALID:", password_valid)


asyncio.run(test_authenticate())