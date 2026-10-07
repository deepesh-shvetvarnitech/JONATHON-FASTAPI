from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from passlib.context import CryptContext

from src.auth.models import User
from src.auth.schemas import UserCreateModel


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class UserService:

    async def user_exists(
        self,
        email: str,
        session: AsyncSession,
    ) -> bool:

        statement = select(User).where(
            User.email == email
        )

        result = await session.exec(statement)

        user = result.first()

        return user is not None

    async def get_user_by_email(
        self,
        email: str,
        session: AsyncSession,
    ):

        statement = select(User).where(
            User.email == email
        )

        result = await session.exec(statement)

        return result.first()

    async def get_user_by_username(
        self,
        username: str,
        session: AsyncSession,
    ):

        statement = select(User).where(
            User.username == username
        )

        result = await session.exec(statement)

        return result.first()

    async def create_user(
        self,
        user_data: UserCreateModel,
        session: AsyncSession,
    ):

        hashed_password = pwd_context.hash(
            user_data.password
        )

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            password_hash=hashed_password,
        )

        session.add(new_user)

        await session.commit()

        await session.refresh(new_user)

        return new_user

    async def authenticate_user(
        self,
        email: str,
        password: str,
        session: AsyncSession,
    ):

        user = await self.get_user_by_email(
            email,
            session,
        )

        if user is None:
            return None

        password_valid = pwd_context.verify(
            password,
            user.password_hash,
        )

        if not password_valid:
            return None

        return user