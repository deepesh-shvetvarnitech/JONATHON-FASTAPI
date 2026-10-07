from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from src.books.schemas import Book


class UserCreateModel(BaseModel):

    username: str

    email: EmailStr

    first_name: str

    last_name: str

    password: str


class UserLoginModel(BaseModel):

    email: EmailStr

    password: str


class UserModel(BaseModel):

    uid: UUID

    username: str

    email: EmailStr

    first_name: str

    last_name: str

    role: str

    is_verified: bool

    created_at: datetime

    update_at: datetime


class UserBooksModel(UserModel):

    books: list[Book]