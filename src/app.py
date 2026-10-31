"""
Data Verven - Glen Mampaey (Streamlit GUI)
==========================================
Run met:  streamlit run src/app.py

Dit is de GUI versie van de verf inventaris tool.
Hieronder staan de GUI componenten die je moet invullen.
"""

import streamlit as st
import csv
import os
import io

# Pad naar de data bestanden
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
PROJECTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "projects")
INVENTORY_CSV = os.path.join(DATA_DIR, "inventory.csv")


# ================================
# DEZE FUNCTIES KOMEN UIT main.py 
# ================================
def load_inventory(filepath=INVENTORY_CSV):
    paints = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['aantal'] = int(row['aantal'])
            paints.append(row)
    return paints


def search_paint(paints, query):
    results = []
    query = query.lower()
    for p in paints:
        if (query in p['kleurnaam'].lower() or
            query in p['artikelnummer'].lower() or
            query in p['volledig_nummer'].lower()):
            results.append(p)
    return results


def shopping_list(paints, project_file):
    must_buy = []
    with open(project_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for item in reader:
            volledig = item['volledig_nummer']
            nodig = int(item['aantal_nodig'])
            gevonden = None
            for p in paints:
                if p['volledig_nummer'] == volledig:
                    gevonden = p
                    break
            if gevonden is None:
                must_buy.append({
                    'kleurnaam': item['kleurnaam'],
                    'volledig_nummer': volledig,
                    'status': 'NIET IN VOORRAAD',
                    'nodig': nodig,
                    'heeft': 0,
                    'tekort': nodig
                })
            elif gevonden['aantal'] < nodig:
                must_buy.append({
                    'kleurnaam': item['kleurnaam'],
                    'volledig_nummer': volledig,
                    'status': 'TE WEINIG',
                    'nodig': nodig,
                    'heeft': gevonden['aantal'],
                    'tekort': nodig - gevonden['aantal']
                })
    return must_buy


# ============================================================
# GUI CODE - Hier bouw jij de interface!
# ============================================================
# Handige Streamlit functies die je kan gebruiken:
#
#   st.title("Tekst")             → Grote titel
#   st.sidebar                    → Menu aan de linkerkant
#   st.text_input("Label")        → Tekst invoerveld
#   st.selectbox("Label", lijst)  → Dropdown menu
#   st.button("Tekst")            → Knop
#   st.dataframe(tabel)           → Mooie tabel tonen
#   st.metric("Label", waarde)    → Cijfer tonen
#   st.write("Tekst")             → Gewoon tekst tonen
#   st.success/warning/error()    → Gekleurde melding
#   st.tabs(["Tab1", "Tab2"])     → Tabs maken


def main():
    # TODO 1: Zet een titel bovenaan
    st.title("Verfjes data")
    
    # Laad de voorraad
    paints = load_inventory()
    
    # TODO 3: Maak een zijbalk (sidebar) met een menu
    # Hint:
    st.sidebar.title("Menu")
    keuze = st.sidebar.radio("Kies:", ["Hoofd menu", "Zoeken", "Voorraad", "Bestellijst"])
    # TODO 2: Toon stats bovenaan (hoeveel in voorraad, hoeveel niet)
    in_voorraad = len([p for p in paints if p['aantal'] > 0])
    niet_in_voorraad = len([p for p in paints if p['aantal'] == 0])
    if keuze == "Hoofd menu":
        st.metric("In voorraad", in_voorraad) 
        st.metric("Niet in voorraad", niet_in_voorraad)
        
    # TODO 4: 
    if keuze == "Zoeken":
        query = st.text_input("Zoek verf: ")
        if query:
            results = search_paint(paints, query)
            st.write(f"gevonde: {len(results)} verven")
            st.dataframe(results)
    
    # TODO 5: 
    if keuze == "Voorraad":
    # Maak een lijst met alleen naam + nummer
        in_voorraad = [p for p in paints if p['aantal'] > 0]
        namen = [f"{p['kleurnaam']} ({p['volledig_nummer']})" for p in in_voorraad]
    
        geselecteerd = st.selectbox("Kies een verf:", namen)
    st.dataframe(in_voorraad)
    
    # TODO 6:
    if keuze == "Bestellijst":
        if bestand is not None:
            bestand = st.file_uploader("Upload een excel bestand", type=["csv"])
            content = bestand.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(content))
            must_buy = []
            for item in reader:
                st.dataframe(must_buy)
    #   - Laat gebruiker een project CSV kiezen
    #   - Bereken de bestellijst met shopping_list()
    #   - Toon wat papa moet kopen
    pass

if __name__ == "__main__":
    main()