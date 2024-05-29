import magyar


def keres_helyseg(magyar_nev):
    magyar_nev = magyar_nev.strip().capitalize()  # Biztosítjuk, hogy a név nagy kezdőbetűs legyen
    hatarontuli = magyar.hatarontuli

    for adat in hatarontuli:
        if magyar_nev in adat:
            mai_hivatalos_nev = adat[magyar_nev]['mai_hivatalos_nev']
            orszag = adat[magyar_nev]['orszag']
            print(f"Település: {magyar_nev}")
            print(f"Mai hivatalos név: {mai_hivatalos_nev}")
            print(f"Ország: {orszag}")
            return
    print("A megadott helységnév nem található a szótárban.")


def main():
    while True:
        magyar_nev = input("Adjon meg egy magyar településnevet (vagy 'exit' a kilépéshez): ").strip()
        if magyar_nev.lower() == 'exit':
            break
        keres_helyseg(magyar_nev)


if __name__ == '__main__':
    main()