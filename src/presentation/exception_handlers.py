from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.domain.exceptions import (
    AccountFrozenException,
    ConflictException,
    InsufficientFundsException,
    NotFoundException,
)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(NotFoundException, _not_found_handler)  # type: ignore[arg-type]
    app.add_exception_handler(ConflictException, _conflict_handler)
    app.add_exception_handler(AccountFrozenException, _conflict_handler)
    app.add_exception_handler(InsufficientFundsException, _unprocessable_handler)


def _not_found_handler(_: Request, exc: NotFoundException) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


def _conflict_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})


def _unprocessable_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": str(exc)})
