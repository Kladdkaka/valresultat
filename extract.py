import zipfile
from pathlib import Path
import json
import pandas as pd

path = Path('data', 'p/kf/Val_20220911_preliminar_1480_KF/Val_20220911_preliminar_rostfordelning_1480_KF.json')

data = json.loads(path.read_text())

entries = []
for distrikt in data['valdistrikt']:

  rostfordelning = distrikt['rostfordelning']

  if rostfordelning is None:
    continue

  valdistriktskod = distrikt['valdistriktskod']

  entry = {}
  entry['valdistriktskod'] = valdistriktskod
  
  roster_paverka_mandat = rostfordelning['rosterPaverkaMandat']

  for rost in roster_paverka_mandat['partiRoster']:
    entry[rost['partiforkortning']] = rost['andelRoster']
  
  entry['OVRIGA'] = roster_paverka_mandat['rosterOvrigaPartier']['andelOvriga'] if 'andelOvriga' in roster_paverka_mandat['rosterOvrigaPartier'] else 0.0

  entries.append(entry)

pd.DataFrame(entries).to_csv('data/rostfordelning_2022.csv', index=False)