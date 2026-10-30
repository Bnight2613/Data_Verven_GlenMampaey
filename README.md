# Data Verven - Glen Mampaey

Verf inventaris en bestellijst applicatie voor scale modeling.

## Doel

- Bijhouden welke verf papa al heeft (voorraad)
- Zoeken naar specifieke verf
- Per project bekijken welke verf nog gekocht moet worden

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

## Structuur

```
Data_Verven_GlenMampaey/
├── data/
│   ├── stock_verven_Datasheet.xlsx   # Originele Excel
│   └── inventory.csv                 # CSV export (425 verven)
├── projects/                         # Project bestanden (welke verf nodig per model)
│   └── example_project.csv
├── src/
│   └── main.py                       # Hoofdprogramma
├── .gitignore
└── requirements.txt
```

## Gebruik

```bash
# Installeer dependencies
pip install -r requirements.txt

# Start het programma
python src/main.py
```
