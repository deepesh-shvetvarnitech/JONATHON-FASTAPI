from typing import Any, List

from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.auth.models import User
from src.auth.service import UserService
from src.db.redis import token_in_blocklist

from .utils import decode_token

from src.errors import (
    InvalidToken,
    AccessTokenRequired,
    RefreshTokenRequired,
    InsufficientPermission,
)


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self,
        request: Request,
    ) -> dict:

        creds: HTTPAuthorizationCredentials = await super().__call__(
            request
        )

        if creds is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization token is required",
            )

        token = creds.credentials

        token_data = decode_token(token)

        if not self.token_valid(token):

            raise InvalidToken()

        if await token_in_blocklist(token_data["jti"]):

            raise InvalidToken()

        self.verify_token_data(token_data)

        return token_data

    def token_valid(
        self,
        token: str,
    ) -> bool:

        token_data = decode_token(token)

        return token_data is not None

    def verify_token_data(
        self,
        token_data: dict,
    ):

        raise NotImplementedError(
            "Please override this method in child classes"
        )


class AccessTokenBearer(TokenBearer):

    def verify_token_data(
        self,
        token_data: dict,
    ) -> None:

        if token_data and token_data.get("refresh"):

            raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):

    def verify_token_data(
        self,
        token_data: dict,
    ) -> None:

        if token_data and not token_data.get("refresh"):

            raise RefreshTokenRequired()


user_service = UserService()


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):

    user_email = token_details["user"]["email"]

    user = await user_service.get_user_by_email(
        user_email,
        session,
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


class RoleChecker:

    def __init__(
        self,
        allowed_roles: List[str],
    ) -> None:

        self.allowed_roles = allowed_roles

    def __call__(
        self,
        current_user: User = Depends(get_current_user),
    ) -> Any:

        if current_user.role in self.allowed_roles:

            return True

        raise InsufficientPermission()