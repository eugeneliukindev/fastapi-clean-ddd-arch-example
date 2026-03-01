class DomainException(Exception):
    pass


class NotFoundException(DomainException):
    pass


class ConflictException(DomainException):
    pass


class InsufficientFundsException(DomainException):
    pass


class AccountFrozenException(DomainException):
    pass
