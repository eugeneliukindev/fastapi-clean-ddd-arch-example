from pydantic import BaseModel


class ApiResponse[T](BaseModel):
    data: T
    message: str | None = None
