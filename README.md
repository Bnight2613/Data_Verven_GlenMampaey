# Data Verven - Glen Mampaey

Verf inventaris en bestellijst applicatie voor scale modeling.
Gemaakt voor papa om zijn verfvoorraad bij te houden en te weten welke verf hij nog moet kopen per project.

## Functies

- 🏠 **Hoofdmenu** — Overzicht van voorraad (hoeveel in/uit voorraad, per reeks)
- 🔍 **Zoeken** — Zoek verf op kleurnaam, artikelnummer of volledig nummer
- 📦 **Voorraad** — Toon alle verven die papa al heeft in een tabel
- 📋 **Bestellijst** — Upload een project CSV en zie welke verf papa nog moet kopen + download de bestellijst
- ✏️ **Voorraad aanpassen** — Pas het aantal per verf aan in een tabel en sla op; wordt direct teruggeschreven naar de Excel (`stock_verven_Datasheet.xlsx`, sheet `verfvoorraad`) én naar `inventory.csv`

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
- De startdata staat op **0 / Nee** — vul zelf in wat er in je voorraad zit via de tab *Voorraad aanpassen*.

### Waar staat mijn data?

Je eigen voorraaddata staat **buiten de app-map**, in:

```
C:\Users\<jouw-gebruikersnaam>\VerfjesData\
```

Bij de eerste start kopieert de app de startdata (aantallen op 0) automatisch naar die map.
Daardoor gaat je data **niet** verloren bij een update: je hoeft alleen de app-map te vervangen,
je voorraad blijft in `VerfjesData` staan.
Om je data te back-uppen: kopieer de map `VerfjesData` naar een veilige plek.

## Structuur

```
Data_Verven_GlenMampaey/
├── data/                             # Alleen startdata (aantallen op 0) — niet je eigen data!
│   ├── stock_verven_Datasheet.xlsx   # Start-Excel
│   └── inventory.csv                 # Start-CSV (425 verven, allemaal 0)
# Je eigen data staat in: %USERPROFILE%\VerfjesData\
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

### Makkelijk starten (dubbelklik)

Dubbelklik op **`Start_App.bat`** (in de hoofdmap van het project).
Die start de web app en opent automatisch je browser.
Je kunt er ook een snelkoppeling van op je bureaublad zetten:
rechtermuisknop op het bestand → *Verzenden naar* → *Bureaublad (snelkoppeling maken)*.

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
