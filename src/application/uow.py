from collections.abc import AsyncGenerator
from types import TracebackType
from typing import Annotated, Self

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.account import IAccountRepository
from src.infrastructure.database import SessionDep
from src.infrastructure.repositories.account import SQLAlchemyAccountRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.accounts: IAccountRepository = SQLAlchemyAccountRepository(session)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            await self.rollback()

    @classmethod
    async def getter(cls, session: SessionDep) -> AsyncGenerator[Self, None]:
        async with cls(session) as self:
            yield self


UoWDep = Annotated[UnitOfWork, Depends(UnitOfWork.getter)]
