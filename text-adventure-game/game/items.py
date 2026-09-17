from dataclasses import dataclass


@dataclass
class Item:
    name: str
    description: str = ""

class Weapon(Item):
    def __init__(self, name, description, damage):
        super().__init__(name, description)
        self.damage = damage

    def use(self):
        return f"You swing the {self.name}, dealing {self.damage} damage!"

class Potion(Item):
    def __init__(self, name, description, healing_amount):
        super().__init__(name, description)
        self.healing_amount = healing_amount

    def use(self):
        return f"You drink the {self.name}, healing {self.healing_amount} health!"