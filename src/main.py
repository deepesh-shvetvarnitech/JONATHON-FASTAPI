# from fastapi import FastAPI, status
# from fastapi.exceptions import HTTPException
# from pydantic import BaseModel
# from typing import List
# from .book_data import books
# from .schemas import Book, BookUpdateModel
# app = FastAPI()






# @app.get("/books", response_model=List[Book])
# async def get_all_books():
#     return books


# @app.post("/books", status_code=status.HTTP_201_CREATED)
# async def create_a_book(book_data: Book) -> dict:
#     new_book = book_data.model_dump()
#     books.append(new_book)
#     return new_book


# @app.get("/books/{book_id}")
# async def get_books(book_id: int) -> dict:
#     for book in books:
#         if book["id"] == book_id:
#             return book

#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Book not found"
#     )


# @app.patch("/books/{book_id}")
# async def update_books(
#     book_id: int,
#     book_update_data: BookUpdateModel
# ) -> dict:

#     for book in books:
#         if book["id"] == book_id:
#             book["title"] = book_update_data.title
#             book["author"] = book_update_data.author
#             book["publisher"] = book_update_data.publisher
#             book["page_count"] = book_update_data.page_count
#             book["language"] = book_update_data.language

#             return book

#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Book not found"
#     )


# @app.delete("/books/{book_id}")
# async def delete_books(book_id: int) -> dict:

#     for book in books:
#         if book["id"] == book_id:
#             books.remove(book)

#             return {
#                 "message": "Book deleted successfully"
#             }

#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Book not found"
#     )
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.db.main import init_db

from src.books.routes import book_router

from src.auth.routes import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    await init_db()

    yield


app = FastAPI(
    title="Bookly",
    description="A simple book management API",
    version="v1",
    lifespan=lifespan,
)


app.include_router(
    book_router,
    prefix="/api/v1/books",
    tags=["books"],
)


app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["auth"],
)