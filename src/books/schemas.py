
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Book(BaseModel):
    uid: UUID
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str
    created_at: datetime
    update_at: datetime


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    published_date: datetime | None = None
    page_count: int | None = None
    language: str | None = None