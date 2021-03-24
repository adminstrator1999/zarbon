from enum import Enum


class OrderPaymentType(Enum):
    cash = "cash"
    credit_card = "credit_card"
    money_transfer = "money_transfer"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class OrderStatus(Enum):
    ordered = "ordered"
    delivered = "delivered"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class FailedProductStatus(Enum):
    valid = "valid"
    invalid = "invalid"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
