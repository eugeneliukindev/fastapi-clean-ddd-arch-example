from src.application.interfaces.base import BaseRepository
from src.domain.entities.account import Account


class IAccountRepository(BaseRepository[Account]):
    pass
