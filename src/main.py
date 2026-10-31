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
    paints = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['aantal'] = int(row['aantal'])
            paints.append(row)
    return paints



# ============================================================
# FUNCTIE 2: Zoek verf
# ============================================================
def search_paint(paints, query):
    results=[]
    query = query.lower()
    for p in paints:
        if (query in p['kleurnaam'].lower() or 
            query in p['artikelnummer'].lower() or 
            query in p['volledig_nummer'].lower()):
            results.append(p)
    return results


# ============================================================
# FUNCTIE 3: Toon wat papa al heeft
# ============================================================
def show_in_stock(paints):
    in_stock = [p for p in paints if p['aantal'] > 0]
    print(f"In voorraad: {len(in_stock)} verven\n")
    for p in in_stock:
        print(f"  {p['kleurnaam']} | {p['volledig_nummer']} | Aantal: {p['aantal']}")



# ============================================================
# FUNCTIE 4: Toon wat papa niet heeft
# ============================================================
def show_out_of_stock(paints):
    out_of_stock = [p for p in paints if p['aantal'] == 0]
    print(f"Niet in voorraad: {len(out_of_stock)} verven\n")
    for p in out_of_stock:
        print(f"  {p['kleurnaam']} | {p['volledig_nummer']}")



# ============================================================
# FUNCTIE 5: Wat moet papa kopen voor een project?
# ============================================================
def shopping_list(paints, project_file):
    must_buy = []
    with open(project_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for item in reader:
            volledig = item['volledig_nummer']
            nodig = int(item['aantal_nodig'])
            
            # Zoek deze verf in de voorraad
            gevonden = None
            for p in paints:
                if p['volledig_nummer'] == volledig:
                    gevonden = p
                    break
            
            if gevonden is None:
                must_buy.append(f"{item['kleurnaam']} ({volledig}) - NIET IN VOORRAAD (nodig: {nodig})")
            elif gevonden['aantal'] < nodig:
                tekort = nodig - gevonden['aantal']
                must_buy.append(f"{item['kleurnaam']} ({volledig}) - Koop er {tekort} extra (heeft: {gevonden['aantal']}, nodig: {nodig})")
    
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