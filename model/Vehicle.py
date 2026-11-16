from enum import Enum, auto

class Vehicle(Enum):
    AUTOCAR = auto()
    E_AUTOCAR = auto()
    MINIBUS = auto()
    E_MINIBUS = auto()

    @classmethod
    def all(cls):
        return list(cls)