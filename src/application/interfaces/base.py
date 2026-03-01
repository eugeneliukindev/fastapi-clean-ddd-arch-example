from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.base import BaseEntity


class BaseRepository[E: BaseEntity](ABC):
    @abstractmethod
    async def get(self, id_: UUID) -> E | None:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> list[E]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, entity: E) -> E:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: E) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id_: UUID) -> E | None:
        raise NotImplementedError
