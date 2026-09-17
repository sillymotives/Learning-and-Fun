from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Room:
    name: str
    description: str
    exits: Dict[str, str] = field(default_factory=dict)
    items: List[str] = field(default_factory=list)


class World:
    def __init__(self):
        self.locations = {}
        self.current_location = None

    def add_location(self, name, description):
        self.locations[name] = description

    def set_start_location(self, name):
        if name in self.locations:
            self.current_location = name
        else:
            raise ValueError(f"Location '{name}' does not exist.")

    def get_current_location(self):
        return self.current_location, self.locations[self.current_location] if self.current_location else None

    def move_to(self, name):
        if name in self.locations:
            self.current_location = name
        else:
            raise ValueError(f"Location '{name}' does not exist.")