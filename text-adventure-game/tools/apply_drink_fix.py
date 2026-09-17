from pathlib import Path

path = Path(__file__).resolve().parents[1] / "game" / "game.py"
text = path.read_text(encoding="utf-8")

old = '        self.drinks_bought = 0\n'
new = '        self.drinks_bought = 0\n        self.failed_drink_attempts = 0\n'
if new not in text:
    if old not in text:
        raise SystemExit("drinks_bought anchor not found")
    text = text.replace(old, new, 1)

old = '''    def drink_from_bar(self):
        if self.current_room != "tavern":
            print("There is no bar here."); return
'''
new = '''    def _drink_in_wrong_place(self):
        self.failed_drink_attempts += 1
        attempt = self.failed_drink_attempts

        openings = (
            "You reach for a glass that is emphatically not here.",
            "You raise an imaginary pint to absolutely nobody.",
            "You stare hopefully at your empty hand.",
            "You mime taking a long drink from the surrounding atmosphere.",
            "You check the immediate area for emergency ale. Again.",
            "You perform the ancient ritual of looking thirsty at architecture.",
        )
        thoughts = (
            '"Am I an alcoholic?"',
            '"Damn... was there something else in that first drink? Kind of want to, er... drink."',
            '"This is becoming less of a request and more of a lifestyle."',
            '"I do understand that drinks normally require... drinks, right?"',
            '"Maybe the tavern has ruined beverages everywhere else for me."',
            '"I am beginning to miss that deeply suspicious ale."',
            '"At some point thirst became a side quest."',
        )
        room_lines = {
            "root_cellar": "The cellar contains several liquids. Every single one is a terrible candidate.",
            "cave_entrance": "The cave entrance offers darkness, damp stone, and absolutely no table service.",
            "cave_chamber": "The cave contains monsters, bones, and no functioning bar staff.",
            "forest_path": "The forest remains stubbornly unlicensed.",
        }
        milestones = {
            10: "Ten attempts. This has officially become a habit.",
            25: "Twenty-five attempts. You are now conducting beverage research.",
            50: "Fifty attempts. Somewhere, the bartender feels a disturbance in the ale.",
            100: "Attempt 100. This is no longer thirst. This is a longitudinal study.",
        }

        print(f"Attempt {attempt}: {openings[(attempt - 1) % len(openings)]}")
        print(thoughts[(attempt - 1) % len(thoughts)])
        print(room_lines.get(self.current_room, "The universe declines to provide a drink here."))
        if attempt in milestones:
            print(f"[Drink obsession milestone] {milestones[attempt]}")

    def drink_from_bar(self):
        if self.current_room != "tavern":
            self._drink_in_wrong_place(); return
'''
if "    def _drink_in_wrong_place(self):\n" not in text:
    if old not in text:
        raise SystemExit("drink_from_bar anchor not found")
    text = text.replace(old, new, 1)

old = '''        if not self.player.spend_coin(1):
            print('Bartender: "You have no coin left, friend."')
            print('Bartender: "The second drink is always the last one."')
            self.state = "game over"; self.running = False; return
'''
new = '''        if not self.player.spend_coin(1):
            print('Bartender: "You have no coin left, friend."')
            if self.drinks_bought:
                print('Bartender: "The second drink may be the last one, but I am not running a tab."')
            else:
                print('Bartender: "Come back when your pockets make a more convincing argument."')
            return
'''
if new not in text:
    if old not in text:
        raise SystemExit("no-coin branch anchor not found")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
