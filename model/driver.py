from dataclasses import dataclass


@dataclass
class Driver:
    driverId: int
    raceId: int
    position: int

    def __hash__(self):
        return hash(self.driverId)
    def __eq__(self, other):
        return self.driverId == other.driverId