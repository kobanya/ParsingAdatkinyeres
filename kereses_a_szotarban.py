import json

# Szótár betöltése JSON fájlból
with open('helysegnevek_dict.json', 'r', encoding='utf-8') as f:
    helyseg_dict = json.load(f)

# Keresés a szótárban
def keres_helyseg(magyar_nev):
    if magyar_nev in helyseg_dict:
        adat = helyseg_dict[magyar_nev]
        print(f"Magyar név: {magyar_nev}")
        print(f"Mai hivatalos név: {adat['mai_hivatalos_nev']}")
        print(f"Ország: {adat['orszag']}")
    else:
        print("A megadott helységnév nem található a szótárban.")

# Fő program, amely bekéri a felhasználótól a településnevet
def main():
    while True:
        magyar_nev = input("Adjon meg egy magyar településnevet (vagy 'exit' a kilépéshez): ")
        if magyar_nev.lower() == 'exit':
            break
        magyar_nev = magyar_nev.capitalize()  # Az input kezdőbetűjének nagybetűsítése
        keres_helyseg(magyar_nev)

if __name__ == "__main__":
    main()
