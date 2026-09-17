from pathlib import Path

path = Path(__file__).resolve().parents[1] / "game" / "game.py"
text = path.read_text(encoding="utf-8")

old = '''            print("You rub ale across the burning bartender.")
            print("The flames hiss out in a cloud of extremely disappointed steam.")
            self.bartender_on_fire = False
            self.bartender_extinguished = True
            self.bartender_hostile = self.bartender_boot_stolen
            print('Bartender: "..."')
            print('Bartender: "I was warm."')
            if self.bartender_boot_stolen:
                print('Bartender: "And you still have my boot."')
            else:
                print('Bartender: "For one beautiful minute, I understood summer."')
'''
new = '''            print("You rub ale across the burning bartender.")
            print("The ale hisses across him as the flames collapse into a cloud of extremely disappointed steam.")
            self.bartender_on_fire = False
            self.bartender_extinguished = True
            self.bartender_hostile = self.bartender_boot_stolen
            print('Bartender: "..."')
            print('Bartender: "I was warm."')
            if self.bartender_boot_stolen:
                print('Bartender: "You stole my boot, set me on fire, and now you put me out."')
                print('Bartender: "I miss normal customers."')
            else:
                print('Bartender: "Refreshing. I hate it."')
                print('Bartender: "For one beautiful minute, I understood summer."')
'''

if new not in text:
    if old not in text:
        raise SystemExit("extinguish dialogue anchor not found")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
