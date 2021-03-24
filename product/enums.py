from enum import Enum


class ProductType(Enum):
    limited = 'limited'
    unlimited = 'unlimited'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class ProductUnit(Enum):
    kg = 'kilogram'
    litr = 'litr'
    ta = 'dona'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)