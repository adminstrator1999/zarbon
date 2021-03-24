from enum import Enum


class UserRole(Enum):
    CEO = "CEO"
    director = "director"
    commodity_accountant = 'commodity_accountant'
    accountant = 'accountant'
    cashier = 'cashier'
    agent = 'agent'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
