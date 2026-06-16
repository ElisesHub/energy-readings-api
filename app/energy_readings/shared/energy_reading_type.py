from enum import Enum

class EnergyReadingType(str, Enum):
    CONSUMPTION = "consumption"
    GENERATION = "generation"