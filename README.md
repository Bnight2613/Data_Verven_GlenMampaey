# Data Verven - Glen Mampaey

Verf inventaris en bestellijst applicatie voor scale modeling.
Gemaakt voor papa om zijn verfvoorraad bij te houden en te weten welke verf hij nog moet kopen per project.

## Functies

- 🏠 **Hoofdmenu** — Overzicht van voorraad (hoeveel in/uit voorraad, per reeks)
- 🔍 **Zoeken** — Zoek verf op kleurnaam, artikelnummer of volledig nummer
- 📦 **Voorraad** — Toon alle verven die papa al heeft in een tabel
- 📋 **Bestellijst** — Upload een project CSV en zie welke verf papa nog moet kopen + download de bestellijst

## Data

De data komt uit een Excel bestand met 425 verven van verschillende series:

| Reeks | Prefix |
|-------|--------|
| Model Air | 71.xxx |
| Model Color | 70.xxx |
| Metal Color | 77.xxx |
| Primer 200ml | 74.xxx |
| Primer 60ml | 73.xxx |
| Primer 17ml | 70.xxx |
| Enamel Revell | REV-xxx |

### Voorraad stats

- Totaal: 425 verven
- In voorraad: 119
- Niet in voorraad: 306

## Structuur

```
Data_Verven_GlenMampaey/
├── data/
│   ├── stock_verven_Datasheet.xlsx   # Originele Excel
│   └── inventory.csv                 # CSV export (425 verven)
├── projects/                         # Project bestanden (welke verf nodig per model)
│   └── example_project.csv            # Voorbeeld project
├── src/
│   ├── main.py                       # Terminal versie (menu)
│   └── app.py                        # Streamlit GUI versie
├── .gitignore
├── README.md
└── requirements.txt
```

## Installatie

```bash
# Installeer dependencies
pip install -r requirements.txt
```

## Gebruik

### GUI versie (Streamlit)

```bash
# Start de web app
python -m streamlit run src/app.py
```

 Dit opent je browser met de applicatie.

### Terminal versie

```bash
# Start het programma in de terminal
python src/main.py
```

## Project CSV formaat

Maak een CSV bestand aan in de `projects/` map voor elk model dat papa wil bouwen:

```csv
kleurnaam,reeks,volledig_nummer,aantal_nodig
Model Air - White,Model Air,71.001,2
Model Air - Yellow,Model Air,71.002,1
Model Air - Blue,Model Air,71.004,3
```

| Kolom | Beschrijving | Voorbeeld |
|-------|-------------|----------|
| kleurnaam | Naam van de verf | Model Air - White |
| reeks | Welke serie | Model Air |
| volledig_nummer | Artikelnummer | 71.001 |
| aantal_nodig | Hoeveel potjes nodig | 2 |

Upload dit bestand in de app via de Bestellijst tab om te zien wat papa nog moet kopen.

## Gemaakt met

- **Python** — Programmeertaal
- **Streamlit** — Web GUI framework
- **openpyxl** — Excel bestanden lezen
- **pandas** — Data verwerking
