from typing import Annotated
from uuid import UUID

from fastapi import Depends

from src.application.uow import UoWDep
from src.domain.entities.account import Account
from src.domain.exceptions import NotFoundException
from src.domain.value_objects.money import Money


class AccountService:
    def __init__(self, uow: UoWDep) -> None:
        self.uow = uow

    async def get(self, id_: UUID) -> Account:
        account = await self.uow.accounts.get(id_)
        if not account:
            raise NotFoundException(f"Account {id_} not found")
        return account

    async def create(self, owner: str, initial_balance: int = 0, currency: str = "RUB") -> Account:
        account = await self.uow.accounts.add(
            Account.new(
                owner=owner,
                balance=Money(amount=initial_balance, currency=currency),
            )
        )
        await self.uow.commit()
        return account

    async def deposit(self, id_: UUID, amount: int, currency: str = "RUB") -> Account:
        account = await self.uow.accounts.get(id_)
        if not account:
            raise NotFoundException(f"Account {id_} not found")
        account.deposit(Money(amount=amount, currency=currency))
        await self.uow.accounts.update(account)
        await self.uow.commit()
        return account

    async def withdraw(self, id_: UUID, amount: int, currency: str = "RUB") -> Account:
        account = await self.uow.accounts.get(id_)
        if not account:
            raise NotFoundException(f"Account {id_} not found")
        account.withdraw(Money(amount=amount, currency=currency))
        await self.uow.accounts.update(account)
        await self.uow.commit()
        return account

    async def freeze(self, id_: UUID) -> Account:
        account = await self.uow.accounts.get(id_)
        if not account:
            raise NotFoundException(f"Account {id_} not found")
        account.freeze()
        await self.uow.accounts.update(account)
        await self.uow.commit()
        return account

    async def unfreeze(self, id_: UUID) -> Account:
        account = await self.uow.accounts.get(id_)
        if not account:
            raise NotFoundException(f"Account {id_} not found")
        account.unfreeze()
        await self.uow.accounts.update(account)
        await self.uow.commit()
        return account

    async def delete(self, id_: UUID) -> Account:
        account = await self.uow.accounts.delete(id_)
        if not account:
            raise NotFoundException(f"Account {id_} not found")
        await self.uow.commit()
        return account


AccountServiceDep = Annotated[AccountService, Depends()]
