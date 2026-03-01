from abc import abstractmethod
from typing import Any
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.base import BaseEntity
from src.application.interfaces.base import BaseRepository
from src.infrastructure.models.base import BaseORM


class BaseSQLAlchemyRepository[E: BaseEntity, ORM: BaseORM](BaseRepository[E]):
    model: type[ORM]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abstractmethod
    def _to_entity(self, orm: ORM) -> E:
        raise NotImplementedError

    @abstractmethod
    def _dump(self, entity: E) -> dict[str, Any]:  # orm_field: entity_field
        raise NotImplementedError

    async def get(self, id_: UUID) -> E | None:
        orm = await self.session.get(self.model, id_)
        return self._to_entity(orm) if orm else None

    async def list(self) -> list[E]:
        result = await self.session.execute(select(self.model))
        return [self._to_entity(orm) for orm in result.scalars().all()]

    async def add(self, entity: E) -> E:
        result = await self.session.execute(insert(self.model).values(**self._dump(entity)).returning(self.model))
        return self._to_entity(result.scalar_one())

    async def update(self, entity: E) -> None:
        await self.session.execute(update(self.model), [self._dump(entity)])  # bulk update

    async def delete(self, id_: UUID) -> E | None:
        result = await self.session.execute(delete(self.model).where(self.model.id == id_).returning(self.model))
        orm = result.scalar_one_or_none()
        return self._to_entity(orm) if orm else None
