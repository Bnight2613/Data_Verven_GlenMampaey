"""
Data Verven - Glen Mampaey
==========================
Verf inventaris en bestellijst tool voor scale modeling.

Dit is de startcode. Hieronder staan de functies die je moet invullen.
Lees de comments bij elke functie voor uitleg.
"""

import csv
import os

# Pad naar de data bestanden
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
PROJECTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "projects")
INVENTORY_CSV = os.path.join(DATA_DIR, "inventory.csv")


# ============================================================
# FUNCTIE 1: Laad de voorraad vanuit CSV
# ============================================================
def load_inventory(filepath=INVENTORY_CSV):
    """
    Leest inventory.csv en geeft een lijst van dictionaries terug.

    Elke paint heeft:
      - kleurnaam     (bijv. "Model Air - Yellow")
      - artikelnummer (bijv. "002")
      - reeks         (bijv. "Model Air")
      - volledig_nummer (bijv. "71.002")
      - in_voorraad   (bijv. "Ja" of "Nee")
      - aantal        (bijv. 3)
      - bestellen     (bijv. "Ja" of "Nee")
      - aantal_bestellen
      - gewenst_aantal

    TODO: Lees het CSV bestand en geef de data terug.
    Hint: Gebruik de csv module of pandas.
    """
    paints = []
    # Jouw code hier...
    return paints


# ============================================================
# FUNCTIE 2: Zoek verf
# ============================================================
def search_paint(paints, query):
    """
    Zoek verf op kleurnaam, artikelnummer, of volledig nummer.

    Bijv:
      search_paint(paints, "Yellow")       -> zoekt op naam
      search_paint(paints, "71.002")       -> zoekt op volledig nummer
      search_paint(paints, "002")          -> zoekt op artikelnummer

    TODO: Filter de paints lijst op de zoekopdracht.
    """
    results = []
    # Jouw code hier...
    return results


# ============================================================
# FUNCTIE 3: Toon wat papa al heeft
# ============================================================
def show_in_stock(paints):
    """
    Toon alle verven waar aantal > 0 (in voorraad).

    TODO: Filter en print de verven die in voorraad zijn.
    """
    # Jouw code hier...
    pass


# ============================================================
# FUNCTIE 4: Toon wat papa niet heeft
# ============================================================
def show_out_of_stock(paints):
    """
    Toon alle verven waar aantal = 0 (niet in voorraad).

    TODO: Filter en print de verven die NIET in voorraad zijn.
    """
    # Jouw code hier...
    pass


# ============================================================
# FUNCTIE 5: Wat moet papa kopen voor een project?
# ============================================================
def shopping_list(paints, project_file):
    """
    Lees een project CSV (welke verven nodig zijn) en vergelijk
    met de voorraad. Geef terug wat papa nog moet kopen.

    Een project CSV ziet er zo uit:
      kleurnaam,reeks,volledig_nummer,aantal_nodig

    TODO:
      1. Lees het project bestand
      2. Voor elke verf in het project, check of papa het al heeft
      3. Als papa het niet heeft (of niet genoeg), voeg toe aan de bestellijst
      4. Print de bestellijst
    """
    must_buy = []
    # Jouw code hier...
    return must_buy


# ============================================================
# HOOFDMENU
# ============================================================
def main():
    print("=" * 50)
    print("  Data Verven - Glen Mampaey")
    print("=" * 50)
    print()

    paints = load_inventory()
    print(f"Voorraad geladen: {len(paints)} verven")
    print()

    while True:
        print("--- Menu ---")
        print("1. Zoek verf")
        print("2. Toon wat papa al heeft")
        print("3. Toon wat papa niet heeft")
        print("4. Bestellijst voor een project")
        print("5. Stoppen")
        print()

        keuze = input("Kies een optie (1-5): ").strip()
        print()

        if keuze == "1":
            query = input("Zoekterm: ").strip()
            results = search_paint(paints, query)
            for p in results:
                print(f"  {p['kleurnaam']} | {p['volledig_nummer']} | Voorraad: {p['aantal']}")

        elif keuze == "2":
            show_in_stock(paints)

        elif keuze == "3":
            show_out_of_stock(paints)

        elif keuze == "4":
            project_name = input("Project bestand (bijv. example_project.csv): ").strip()
            project_file = os.path.join(PROJECTS_DIR, project_name)
            if os.path.exists(project_file):
                must_buy = shopping_list(paints, project_file)
                print(f"\nTe kopen: {len(must_buy)} verven")
                for p in must_buy:
                    print(f"  {p}")
            else:
                print(f"Bestand niet gevonden: {project_file}")

        elif keuze == "5":
            print("Tot ziens!")
            break

        else:
            print("Ongeldige keuze.")

        print()


if __name__ == "__main__":
    main()