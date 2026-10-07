import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from src.auth.models import User


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )

    title: str

    author: str

    publisher: str

    published_date: datetime = Field(
        sa_column=Column(pg.TIMESTAMP)
    )

    page_count: int

    language: str

    user_uid: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="users.uid",
    )

    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.utcnow,
        )
    )

    update_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.utcnow,
        )
    )

    user: Optional["User"] = Relationship(
        back_populates="books"
    )