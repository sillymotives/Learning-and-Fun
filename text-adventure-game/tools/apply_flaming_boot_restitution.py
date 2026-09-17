from pathlib import Path

path = Path('game/game.py')
text = path.read_text(encoding='utf-8')
anchor = '''    def _handle_stateful_interaction(self, verb, item, target):\n        if self.current_room != "tavern":\n            return False\n        if item == "torch" and target == "bartender":\n'''
replacement = '''    def _handle_stateful_interaction(self, verb, item, target):\n        if self.current_room != "tavern":\n            return False\n        if (\n            item == "bartender's left boot"\n            and target == "bartender"\n            and self.boot_on_fire\n            and self.bartender_extinguished\n        ):\n            print("You offer the bartender his left boot.")\n            print("It is on fire.")\n            print("He looks at the boot.")\n            print("He looks at you.")\n            print("He looks back at the boot.")\n            print('Bartender: "That is not what restitution means."')\n            print("The cuff brushes his apron.")\n            print("FWOOMPH.")\n            self.bartender_on_fire = True\n            self.bartender_extinguished = False\n            self.bartender_hostile = True\n            print("He closes his eyes.")\n            print('Bartender: "...warm."')\n            print('Bartender: "I hate that this helped."')\n            self._record_optional_interaction(verb, item, target)\n            return True\n        if item == "torch" and target == "bartender":\n'''
if text.count(anchor) != 1:
    raise SystemExit(f'expected one anchor, found {text.count(anchor)}')
path.write_text(text.replace(anchor, replacement, 1), encoding='utf-8')
