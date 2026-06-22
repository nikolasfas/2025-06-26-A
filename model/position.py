from dataclasses import dataclass


@dataclass
class Position:
    circuitId: int
    raceId: int
    year: int
    driverId: int
    position: int
