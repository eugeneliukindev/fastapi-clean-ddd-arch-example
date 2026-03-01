from sqlalchemy.orm import Mapped

from .base import BaseORM


class AccountORM(BaseORM):
    __tablename__ = "accounts"

    owner: Mapped[str]
    balance: Mapped[int]
    currency: Mapped[str]
    status: Mapped[str]
