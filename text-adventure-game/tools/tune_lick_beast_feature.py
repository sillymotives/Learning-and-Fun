from pathlib import Path

path = Path('game/game.py')
text = path.read_text(encoding='utf-8')
old = '''            print('Bartender: "Take this. They are awful tippers, but better customers than you."')
'''
new = '''            print('Bartender: "Take this drink. They are awful tippers, but better customers than you."')
'''
if text.count(old) != 1:
    raise SystemExit(f'expected one bartender beast-drink line, found {text.count(old)}')
path.write_text(text.replace(old, new, 1), encoding='utf-8')

bartender = Path('game/bartender_dialogue.py')
bartender.write_text(bartender.read_text(encoding='utf-8').rstrip() + '\n', encoding='utf-8')
print('PASS: beast-drink handoff wording and EOF tuned')
