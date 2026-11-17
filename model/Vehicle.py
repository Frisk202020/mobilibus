from enum import Enum, auto

"""
Enum defining all types of vehicles of the company
"""
class Vehicle(Enum):
    AUTOCAR = auto()
    E_AUTOCAR = auto()
    MINIBUS = auto()
    E_MINIBUS = auto()

    @classmethod
    def all(cls):
        return list(cls)