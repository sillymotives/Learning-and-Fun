from .items import Item


class Player:
    def __init__(self, name="Traveller", coins=1):
        self.name = name
        self.coins = coins
        self.inventory = []

    def set_name(self, name: str):
        cleaned = name.strip()
        self.name = cleaned if cleaned else "Traveller"

    def add_coin(self, amount=1):
        self.coins += amount

    def spend_coin(self, amount=1):
        if self.coins < amount:
            return False
        self.coins -= amount
        return True

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item_name: str):
        for item in self.inventory:
            if item.name == item_name:
                self.inventory.remove(item)
                return item
        return None

    def show_inventory(self):
        if not self.inventory:
            print("You are carrying nothing.")
            return

        print("Inventory:")
        for item in self.inventory:
            print(f" - {item.name}: {item.description or 'No description.'}")
        print(f"Coins: {self.coins}")