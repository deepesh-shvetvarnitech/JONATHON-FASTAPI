from datetime import datetime, timezone
import uuid
from typing import TYPE_CHECKING, List

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel, Relationship


if TYPE_CHECKING:
    from src.books.models import Book


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )

    username: str = Field(
        sa_column=Column(
            String,
            nullable=False,
            unique=True,
            index=True,
        )
    )

    email: str = Field(
        sa_column=Column(
            String,
            nullable=False,
            unique=True,
            index=True,
        )
    )

    first_name: str = Field(
        nullable=False
    )

    last_name: str = Field(
        nullable=False
    )

    password_hash: str = Field(
        nullable=False
    )

    role: str = Field(
        sa_column=Column(
            pg.VARCHAR,
            nullable=False,
            server_default="user",
        )
    )

    is_verified: bool = Field(
        default=False,
        nullable=False,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    update_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    books: List["Book"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "lazy": "selectin"
        },
    )