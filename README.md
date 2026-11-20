# Data Verven — Glen Mampaey

## Streamlit Email
Er zal eerst gevraagt worden voor een email deze moet u ingeven om verder te kunnen.

Een applicatie voor het bijhouden van de verfvoorraad en het opstellen van een bestellijst
bij het scale modeling van modellen. Het programma vergelijkt de voorraad met de vereiste
verven per project en geeft aan welke verfen nog aangeschaft moeten worden.

## Functionaliteit

- **Hoofdmenu** — Overzicht van de voorraad, onderverdeeld per reeks.
- **Zoeken** — Verf zoeken op kleurnaam, artikelnummer of volledig nummer.
- **Voorraad** — Alle verfen in de voorraad, weergegeven in een tabel.
- **Bestellijst** — Upload een project-CSV en zie welke verfen nog aangeschaft moeten worden;
  de bestellijst kan worden gedownload.
- **Voorraad aanpassen** — Aantallen per verf aanpassen in een tabel en opslaan.
  De wijzigingen worden teruggeschreven naar zowel
  `stock_verven_Datasheet.xlsx` (sheet `verfvoorraad`) als `inventory.csv`.

## Data

De data bestaat uit een Excel-bestand met 425 verfen uit verschillende series.

| Reeks | Prefix |
|-------|--------|
| Model Air | 71.xxx |
| Model Color | 70.xxx |
| Metal Color | 77.xxx |
| Primer 200ml | 74.xxx |
| Primer 60ml | 73.xxx |
| Primer 17ml | 70.xxx |
| Enamel Revell | REV-xxx |

De startdata staat standaard op `0` / `Nee`. Vul via de tab *Voorraad aanpassen*
zelf in welke verfen in de voorraad aanwezig zijn.

### Locatie van de eigen data

De eigen voorraaddata wordt opgeslagen buiten de app-map, op de volgende locatie:

```
C:\Users\<gebruikersnaam>\VerfjesData\
```

Bij de eerste start kopieert de applicatie de startdata (aantallen op `0`) automatisch
naar deze map. Hierdoor blijft de eigen voorraad behouden bij een update: vervang alleen
de app-map, de voorraaddata blijft in `VerfjesData` staan. Voor een back-up is het
voldoende om de map `VerfjesData` te kopiëren naar een veilige locatie.

## Projectstructuur

```
Data_Verven_GlenMampaey/
├── data/                             # Alleen startdata (aantallen op 0)
│   ├── stock_verven_Datasheet.xlsx   # Start-Excel
│   └── inventory.csv                 # Start-CSV (425 verfen, allemaal 0)
├── projects/                         # Projectbestanden (verf per model)
│   └── example_project.csv           # Voorbeeldproject
├── src/
│   ├── main.py                       # Terminalversie (menu)
│   └── app.py                        # Streamlit-versie (web GUI)
├── .gitignore
├── README.md
├── requirements.txt
└── Start_App.bat                     # Start de web-app (dubbelklik)

# De eigen voorraaddata staat in: %USERPROFILE%\VerfjesData\
```

## Installatie

```bash
pip install -r requirements.txt
```

## Gebruik

### Web-app starten

Dubbelklik op `Start_App.bat` in de hoofdmap van het project. De web-app start en de
browser opent automatisch. Er kan een snelkoppeling voor worden aangemaakt via:
rechtermuisknop op het bestand, *Verzenden naar*, *Bureaublad (snelkoppeling maken)*.

Alternatief via de terminal:

```bash
python -m streamlit run src/app.py
```

### Terminalversie

```bash
python src/main.py
```

## Project-CSV formaat

Maak voor elk model een CSV-bestand aan in de `projects/` map met de benodigde verfen.

```csv
kleurnaam,reeks,volledig_nummer,aantal_nodig
Model Air - White,Model Air,71.001,2
Model Air - Yellow,Model Air,71.002,1
Model Air - Blue,Model Air,71.004,3
```

| Kolom | Beschrijving | Voorbeeld |
|-------|-------------|----------|
| `kleurnaam` | Naam van de verf | Model Air - White |
| `reeks` | Serie | Model Air |
| `volledig_nummer` | Artikelnummer | 71.001 |
| `aantal_nodig` | Aantal benodigde verfen | 2 |

Upload het bestand via de tab *Bestellijst* om te zien welke verfen nog aangeschaft
moeten worden.

## Gebruikte technologie

- **Python** — programmeertaal
- **Streamlit** — web GUI-framework
- **openpyxl** — lezen en schrijven van Excel-bestanden
- **pandas** — dataverwerking
