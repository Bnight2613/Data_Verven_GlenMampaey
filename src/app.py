"""
Data Verven - Glen Mampaey (Streamlit GUI)
==========================================
Run met:  streamlit run src/app.py

Dit is de GUI versie van de verf inventaris tool.
Hieronder staan de GUI componenten die je moet invullen.
"""

import streamlit as st
import pandas as pd
import openpyxl
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


def load_excel_inventory(uploaded_file):
    """Leest een Excel bestand en geeft de voorraad terug als lijst van dictionaries."""
    # Sla het geüploade bestand tijdelijk op zodat openpyxl het kan lezen
    content = uploaded_file.read()
    wb = openpyxl.load_workbook(io.BytesIO(content), data_only=True)
    ws = wb['verfvoorraad']
    
    paints = []
    for row in ws.iter_rows(min_row=9, max_row=ws.max_row, values_only=True):
        # Kolommen: B(1)=Kleurnaam, C(2)=Artikelnummer, D(3)=Reeks, 
        # E(4)=Volledig nummer, F(5)=In voorraad, G(6)=Aantal
        if row[1] and row[3]:
            try:
                aantal = int(row[6]) if row[6] is not None else 0
            except (ValueError, TypeError):
                aantal = 0
            
            paints.append({
                'kleurnaam': str(row[1]).strip(),
                'artikelnummer': str(row[2]).strip() if row[2] else '',
                'reeks': str(row[3]).strip(),
                'volledig_nummer': str(row[4]).strip() if row[4] else '',
                'in_voorraad': str(row[5]).strip() if row[5] else 'Nee',
                'aantal': aantal,
                'bestellen': str(row[7]).strip() if row[7] else 'Nee',
                'aantal_bestellen': '0',
                'gewenst_aantal': '0'
            })
    
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
#   st.info/warning()             → Gekleurde melding (blauw/oranje, kleurenblind-vriendelijk)
#   st.tabs(["Tab1", "Tab2"])     → Tabs maken


def main():
    # TODO 1: Zet een titel bovenaan
    st.title("Verfjes data")
    
    # Laad de voorraad (van CSV of van geüploade Excel)
    if 'uploaded_paints' in st.session_state:
        paints = st.session_state['uploaded_paints']
    else:
        paints = load_inventory()
    
    # TODO 3: Maak een zijbalk (sidebar) met een menu
    # Hint:
    st.sidebar.title("Menu")
    keuze = st.sidebar.radio("Kies:", ["Hoofd menu", "Zoeken", "Voorraad", "Bestellijst", "Excel uploaden"])
    # TODO 2: Toon stats bovenaan (hoeveel in voorraad, hoeveel niet)
    in_voorraad = len([p for p in paints if p['aantal'] > 0])
    niet_in_voorraad = len([p for p in paints if p['aantal'] == 0])
    if keuze == "Hoofd menu":
        col1, col2 = st.columns(2)
        col1.metric("In voorraad", in_voorraad)
        col2.metric("Niet in voorraad", niet_in_voorraad)
    
        st.write("### Per reeks:")
        reeksen = ["Model Air", "Model Color", "Metal Color", "Primer 17ml", "Primer 60ml", "Primer 200ml", "Enamel Revell"]
        for reeks in reeksen:
            aantal = len([p for p in paints if p['reeks'] == reeks and p['aantal'] > 0])
            st.write(f"- {reeks}: {aantal} in voorraad")


    # TODO 4: 
    if keuze == "Zoeken":
        query = st.text_input("Zoek verf: ")
        if query:
            results = search_paint(paints, query)
            st.write(f"gevonden: {len(results)} verven")
        
            for p in results:
                if p['aantal'] > 0:
                    st.info(f"🔵 IN VOORRAAD: {p['kleurnaam']} | {p['volledig_nummer']} | Aantal: {p['aantal']}")
                else:
                    st.warning(f"🟠 NIET IN VOORRAAD: {p['kleurnaam']} | {p['volledig_nummer']}")

    # TODO 5: 
    if keuze == "Voorraad":
        reeksen = ["Alle"] + list(set(p['reeks'] for p in paints))
        reeks_filter = st.selectbox("Filter op reeks:", reeksen)
    
        if reeks_filter == "Alle":
            toon_verven = paints
        else:
            toon_verven = [p for p in paints if p['reeks'] == reeks_filter]
    
    # Voeg status toe
        for p in toon_verven:
            p['status'] = "🔵 IN VOORRAAD" if p['aantal'] > 0 else "🟠 NIET IN VOORRAAD"
    
        st.dataframe(toon_verven)


    
    # TODO 6:
    if keuze == "Bestellijst":
        methode = st.radio("Hoe wil je een bestellijst maken?", ["CSV uploaden", "Zelf verven kiezen"])
        
        # --- Optie 1: CSV uploaden (bestaand) ---
        if methode == "CSV uploaden":
            bestand = st.file_uploader("Upload een project CSV:", type=["csv"])
        
            if bestand is not None:
                content = bestand.read().decode('utf-8')
                reader = csv.DictReader(io.StringIO(content))
            
                must_buy = []
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
            
                st.write(f"Te kopen: {len(must_buy)} verven")
                st.dataframe(must_buy)
                st.download_button("Download bestellijst", 
                    pd.DataFrame(must_buy).to_csv(index=False),
                    "bestellijst.csv")
        
        # --- Optie 2: Zelf verven kiezen (nieuw) ---
        if methode == "Zelf verven kiezen":
            st.write("### Kies de verven die je nodig hebt voor je project")
            st.write("")
            
            # Filter op reeks om makkelijker te zoeken
            reeksen = ["Alle"] + list(set(p['reeks'] for p in paints))
            reeks_filter = st.selectbox("Filter op reeks:", reeksen)
            
            if reeks_filter == "Alle":
                keuzes = [f"{p['kleurnaam']} ({p['volledig_nummer']})" for p in paints]
            else:
                keuzes = [f"{p['kleurnaam']} ({p['volledig_nummer']})" for p in paints if p['reeks'] == reeks_filter]
            
            # Laat de gebruiker meerdere verven tegelijk kiezen
            geselecteerd = st.multiselect("Kies je verven:", keuzes)
            
            if geselecteerd:
                # Maak een lijst met de gekozen verven + hoeveelheid
                st.write("### Hoeveel heb je er nodig?")
                
                project_verven = []
                for keuze_verf in geselecteerd:
                    # Haal de volledig_nummer uit de string
                    volledig = keuze_verf.split("(")[-1].rstrip(")")
                    # Vind de verf in de voorraad
                    for p in paints:
                        if p['volledig_nummer'] == volledig:
                            nodig = st.number_input(
                                f"{p['kleurnaam']} ({p['volledig_nummer']})",
                                min_value=1,
                                value=1,
                                key=volledig
                            )
                            project_verven.append({
                                'kleurnaam': p['kleurnaam'],
                                'volledig_nummer': volledig,
                                'reeks': p['reeks'],
                                'aantal_nodig': nodig,
                                'in_voorraad': p['aantal']
                            })
                            break
                
                # Genereer bestellijst
                if st.button("Bereken bestellijst"):
                    must_buy = []
                    heb_al = []
                    
                    for item in project_verven:
                        nodig = item['aantal_nodig']
                        heeft = item['in_voorraad']
                        
                        if heeft == 0:
                            must_buy.append({
                                'kleurnaam': item['kleurnaam'],
                                'volledig_nummer': item['volledig_nummer'],
                                'status': '🟠 NIET IN VOORRAAD',
                                'nodig': nodig,
                                'heeft': 0,
                                'tekort': nodig
                            })
                        elif heeft < nodig:
                            must_buy.append({
                                'kleurnaam': item['kleurnaam'],
                                'volledig_nummer': item['volledig_nummer'],
                                'status': '🟠 TE WEINIG',
                                'nodig': nodig,
                                'heeft': heeft,
                                'tekort': nodig - heeft
                            })
                        else:
                            heb_al.append({
                                'kleurnaam': item['kleurnaam'],
                                'volledig_nummer': item['volledig_nummer'],
                                'status': '🔵 IN VOORRAAD',
                                'nodig': nodig,
                                'heeft': heeft,
                                'tekort': 0
                            })
                    
                    # Toon wat je al hebt
                    st.write(f"### ✅ Al in voorraad: {len(heb_al)} verven")
                    if heb_al:
                        st.dataframe(heb_al)
                    
                    # Toon wat je moet kopen
                    st.write(f"### 🟠 Te kopen: {len(must_buy)} verven")
                    if must_buy:
                        st.dataframe(must_buy)
                        st.download_button("Download bestellijst", 
                            pd.DataFrame(must_buy).to_csv(index=False),
                            "bestellijst.csv")
                    else:
                        st.info("🔵 Je hebt alles in voorraad!")

                    

    # TODO 7: Excel uploaden om voorraad te updaten
    if keuze == "Excel uploaden":
        st.write("### Upload je Excel voorraad bestand")
        st.write("Upload het bestand `stock_verven_Datasheet.xlsx` om de voorraad in de app te updaten.")
        st.write("Dit werkt voor de huidige sessie. Sluit je de app, dan wordt de originele CSV weer gebruikt.")
        st.write("")
        
        excel_bestand = st.file_uploader("Kies je Excel bestand:", type=["xlsx"])
        
        if excel_bestand is not None:
            try:
                nieuwe_voorraad = load_excel_inventory(excel_bestand)
                st.session_state['uploaded_paints'] = nieuwe_voorraad
                st.info(f"✅ Voorraad geladen: {len(nieuwe_voorraad)} verven!")
                
                in_voorraad = len([p for p in nieuwe_voorraad if p['aantal'] > 0])
                niet_in_voorraad = len([p for p in nieuwe_voorraad if p['aantal'] == 0])
                
                col1, col2 = st.columns(2)
                col1.metric("In voorraad", in_voorraad)
                col2.metric("Niet in voorraad", niet_in_voorraad)
                
                st.write("Ga nu naar Zoeken, Voorraad of Bestellijst om de nieuwe data te gebruiken!")
            except Exception as e:
                st.warning(f"⚠️ Fout bij het lezen van het bestand: {e}")


if __name__ == "__main__":
    main()