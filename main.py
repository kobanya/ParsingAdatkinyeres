import requests
from bs4 import BeautifulSoup
import pandas as pd

# Az alap URL, ahonnan az adatokat gyűjtjük
base_url = 'https://sebok2.adatbank.ro/index.php?kezd='

def get_data_from_page(page_number):
    url = f'{base_url}{page_number}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Keresd meg az adatokat tartalmazó táblázatot
    table = soup.find('table')
    if not table:
        print(f"Nem található táblázat az oldalon: {page_number}")
        return []

    rows = table.find_all('tr')
    data = []

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols if ele.text.strip()]  # Üres oszlopok kihagyása
        # Kizárjuk azokat a sorokat, amelyek a fejléc szöveget tartalmazzák
        if len(cols) == 4:
            magyar_nev, magyar_megye, mai_hivatalos_nev, orszag = cols
            if "helységnévtárban szereplő" in magyar_nev.lower():
                continue
            data.append([magyar_nev, mai_hivatalos_nev, orszag])
        elif len(cols) == 3:  # Ha a magyar megye hiányzik
            magyar_nev, mai_hivatalos_nev, orszag = cols
            if "helységnévtárban szereplő" in magyar_nev.lower():
                continue
            data.append([magyar_nev, mai_hivatalos_nev, orszag])

    return data

# Összes oldal feldolgozása
all_data = []
for page_start in range(0, 344*30, 30):  # Feltételezzük, hogy 344 oldal van
    print(f"Processing page starting at: {page_start}")
    page_data = get_data_from_page(page_start)
    all_data.extend(page_data)

# Az összes adat DataFrame-be és CSV fájlba mentése
df = pd.DataFrame(all_data, columns=['Magyar név', 'Mai hivatalos név', 'Ország'])

# További nem kívánt karakterek eltávolítása az egyes oszlopokból
df['Magyar név'] = df['Magyar név'].str.replace('"', '').str.strip()
df['Mai hivatalos név'] = df['Mai hivatalos név'].str.replace('"', '').str.strip()
df['Ország'] = df['Ország'].str.replace('"', '').str.replace('[', '').str.replace(']', '').str.strip()

# Szűrés a nem kívánt sorok eltávolítására
df = df[~df['Magyar név'].str.contains("sebők lászló|Határon túli magyar helységnévtár|Ausztria|10310 helység|helységnévtárban szereplő magyar névalakok|kapcsolódik", case=False, na=False)]
df = df[~df['Mai hivatalos név'].str.contains("sebők lászló|Határon túli magyar helységnévtár|Ausztria|10310 helység|helységnévtárban szereplő magyar névalakok|kapcsolódik", case=False, na=False)]
df = df[~df['Ország'].str.contains("sebők lászló|Határon túli magyar helységnévtár|Ausztria|10310 helység|helységnévtárban szereplő magyar névalakok|kapcsolódik", case=False, na=False)]

# Az üres sorok kiszűrése
df = df.dropna()

# Eltávolítjuk az üres sorokat és oszlopokat
df = df[(df['Magyar név'] != '') & (df['Mai hivatalos név'] != '') & (df['Ország'] != '')]

df.to_csv('szlovakiai_magyar_helysegnevek.csv', index=False, encoding='utf-8')
print("Az adatok sikeresen kinyerve és elmentve a 'szlovakiai_magyar_helysegnevek.csv' fájlba.")
