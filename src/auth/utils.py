from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from src.config import Config


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(
    password: str
) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    user_data: dict,
    expiry: timedelta | None = None,
    refresh: bool = False,
) -> str:

    payload = {
        "user": user_data,

        "exp": (
            datetime.now(timezone.utc)
            + (
                expiry
                if expiry
                else timedelta(
                    minutes=Config.JWT_EXPIRATION_MINUTES
                )
            )
        ),

        "jti": str(
            datetime.now(timezone.utc).timestamp()
        ),

        "refresh": refresh,
    }

    token = jwt.encode(
        payload,
        Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM,
    )

    return token


def decode_token(
    token: str,
) -> dict | None:

    try:
        token_data = jwt.decode(
            token,
            Config.JWT_SECRET_KEY,
            algorithms=[
                Config.JWT_ALGORITHM
            ],
        )

        return token_data

    except jwt.ExpiredSignatureError:
        return None

    except jwt.JWTError:
        return None