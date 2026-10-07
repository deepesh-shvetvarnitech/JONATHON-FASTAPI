from datetime import datetime
from uuid import UUID

from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.models import Book
from src.books.schemas import (
    BookCreateModel,
    BookUpdateModel,
)


class BookService:

    async def get_all_books(
        self,
        session: AsyncSession,
    ):
        statement = select(Book)

        result = await session.exec(statement)

        return result.all()

    async def get_book(
        self,
        book_uid: str,
        session: AsyncSession,
    ):
        statement = select(Book).where(
            Book.uid == book_uid
        )

        result = await session.exec(statement)

        return result.first()

    async def get_user_books(
        self,
        user_uid: str,
        session: AsyncSession,
    ):
        statement = (
            select(Book)
            .where(
                Book.user_uid == UUID(str(user_uid))
            )
            .order_by(
                desc(Book.created_at)
            )
        )

        result = await session.exec(statement)

        return result.all()

    async def create_book(
        self,
        book_data: BookCreateModel,
        user_uid: str,
        session: AsyncSession,
    ):
        book_data_dict = book_data.model_dump()

        new_book = Book(
            title=book_data_dict["title"],
            author=book_data_dict["author"],
            publisher=book_data_dict["publisher"],
            published_date=book_data_dict["published_date"],
            page_count=book_data_dict["page_count"],
            language=book_data_dict["language"],
            user_uid=UUID(str(user_uid)),
        )

        session.add(new_book)

        await session.commit()

        await session.refresh(new_book)

        return new_book

    async def update_book(
        self,
        book_uid: str,
        book_data: BookUpdateModel,
        session: AsyncSession,
    ):
        book = await self.get_book(
            book_uid,
            session,
        )

        if book is None:
            return None

        update_data = book_data.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(
                book,
                key,
                value,
            )

        book.update_at = datetime.now()

        session.add(book)

        await session.commit()

        await session.refresh(book)

        return book

    async def delete_book(
        self,
        book_uid: str,
        session: AsyncSession,
    ):
        book = await self.get_book(
            book_uid,
            session,
        )

        if book is None:
            return None

        await session.delete(book)

        await session.commit()

        return book