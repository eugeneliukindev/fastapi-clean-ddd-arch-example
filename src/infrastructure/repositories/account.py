from typing import Any

from src.application.interfaces.account import IAccountRepository
from src.domain.entities.account import Account, AccountStatus
from src.domain.value_objects.money import Money
from src.infrastructure.models.account import AccountORM
from src.infrastructure.repositories.base import BaseSQLAlchemyRepository


class SQLAlchemyAccountRepository(BaseSQLAlchemyRepository[Account, AccountORM], IAccountRepository):
    model = AccountORM

    def _to_entity(self, orm: AccountORM) -> Account:
        return Account(
            id=orm.id,
            owner=orm.owner,
            balance=Money(amount=orm.balance, currency=orm.currency),
            status=AccountStatus(orm.status),
        )

    def _dump(self, entity: Account) -> dict[str, Any]:
        return {
            "id": entity.id,
            "owner": entity.owner,
            "balance": entity.balance.amount,
            "currency": entity.balance.currency,
            "status": entity.status,
        }
