import pandas as pd
import json

# Az előzőleg kinyert CSV fájl betöltése
df = pd.read_csv('szlovakiai_magyar_helysegnevek.csv')

# Szótár létrehozása
helyseg_dict = {}
for index, row in df.iterrows():
    magyar_nev = row['Magyar név']
    mai_hivatalos_nev = row['Mai hivatalos név']
    orszag = row['Ország']
    helyseg_dict[magyar_nev] = {'mai_hivatalos_nev': mai_hivatalos_nev, 'orszag': orszag}

# Szótár mentése JSON fájlba
with open('helysegnevek_dict.json', 'w', encoding='utf-8') as f:
    json.dump(helyseg_dict, f, ensure_ascii=False, indent=4)

print("A szótár sikeresen létrehozva és elmentve a 'helysegnevek_dict.json' fájlba.")
