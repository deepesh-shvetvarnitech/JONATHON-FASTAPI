from typing import Any, Callable
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

class BooklyException(Exception): pass
class InvalidToken(BooklyException): pass
class RevokedToken(BooklyException): pass
class AccessTokenRequired(BooklyException): pass
class RefreshTokenRequired(BooklyException): pass
class UserAlreadyExists(BooklyException): pass
class InvalidCredentials(BooklyException): pass
class InsufficientPermission(BooklyException): pass
class BookNotFound(BooklyException): pass
class UserNotFound(BooklyException): pass

def create_exception_handler(status_code: int, initial_detail: Any) -> Callable:
    async def exception_handler(request: Request, exc: BooklyException):
        return JSONResponse(content=initial_detail, status_code=status_code)
    return exception_handler

def register_error_handlers(app: FastAPI):
    app.add_exception_handler(UserAlreadyExists, create_exception_handler(status.HTTP_403_FORBIDDEN, {"message": "User with email already exists", "error_code": "user_exists"}))
    app.add_exception_handler(UserNotFound, create_exception_handler(status.HTTP_404_NOT_FOUND, {"message": "User not found", "error_code": "user_not_found"}))
    app.add_exception_handler(BookNotFound, create_exception_handler(status.HTTP_404_NOT_FOUND, {"message": "Book not found", "error_code": "book_not_found"}))
    app.add_exception_handler(InvalidCredentials, create_exception_handler(status.HTTP_400_BAD_REQUEST, {"message": "Invalid Email Or Password", "error_code": "invalid_email_or_password"}))
    app.add_exception_handler(InvalidToken, create_exception_handler(status.HTTP_401_UNAUTHORIZED, {"message": "Token is invalid Or expired", "resolution": "Please get new token", "error_code": "invalid_token"}))
    app.add_exception_handler(RevokedToken, create_exception_handler(status.HTTP_401_UNAUTHORIZED, {"message": "Token is invalid or has been revoked", "resolution": "Please get new token", "error_code": "token_revoked"}))
    app.add_exception_handler(AccessTokenRequired, create_exception_handler(status.HTTP_401_UNAUTHORIZED, {"message": "Please provide a valid access token", "resolution": "Please get an access token", "error_code": "access_token_required"}))
    app.add_exception_handler(RefreshTokenRequired, create_exception_handler(status.HTTP_403_FORBIDDEN, {"message": "Please provide a valid refresh token", "resolution": "Please get a refresh token", "error_code": "refresh_token_required"}))
    app.add_exception_handler(InsufficientPermission, create_exception_handler(status.HTTP_401_UNAUTHORIZED, {"message": "You do not have enough permissions to perform this action", "error_code": "insufficient_permissions"}))

    @app.exception_handler(500)
    async def internal_server_error(request: Request, exc: Exception):
        return JSONResponse(content={"message": "Oops! Something went wrong", "error_code": "server_error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
