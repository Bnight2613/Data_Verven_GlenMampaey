# TODO - Ideeën voor uitbreiding

Hier staan functies die nog toegevoegd kunnen worden aan de app.
Gerangschikt van makkelijk naar moeilijk.

---

## 1. 🔔 Lage voorraad waarschuwing *(Makkelijk)*

Toon verven waar papa bijna doorheen is (aantal = 1). Zo weet hij tijdig nieuwe te kopen.

**Waar:** Hoofdmenu, onder de stats

```python
laag = [p for p in paints if 0 < p['aantal'] <= 1]
if laag:
    st.warning(f"⚠️ {len(laag)} verven bijna op!")
    st.dataframe(laag)
```

---

## 2. 📊 Grafiek van voorraad per reeks *(Makkelijk)*

Een visueel overzicht van hoeveel verf papa per reeks heeft.

**Waar:** Hoofdmenu, onder "Per reeks"

```python
import pandas as pd

reeksen = ["Model Air", "Model Color", "Metal Color", "Primer 17ml", "Primer 60ml", "Primer 200ml", "Enamel Revell"]
data = []
for reeks in reeksen:
    in_stock = len([p for p in paints if p['reeks'] == reeks and p['aantal'] > 0])
    uit_stock = len([p for p in paints if p['reeks'] == reeks and p['aantal'] == 0])
    data.append({"reeks": reeks, "in_voorraad": in_stock, "niet_in_voorraad": uit_stock})

st.bar_chart(pd.DataFrame(data).set_index("reeks"))
```

---

## 3. 🖨️ Print-vriendelijke bestellijst *(Makkelijk)*

De bestellijst opmaken als een nette lijst die papa kan printen en meenemen naar de winkel.

**Waar:** Bestellijst tab, onder de bestellijst

```python
if must_buy:
    st.write("### 🖨️ Print-vriendelijke bestellijst")
    for i, p in enumerate(must_buy, 1):
        st.write(f"{i}. {p['kleurnaam']} ({p['volledig_nummer']}) - {p['status']} - Tekort: {p['tekort']}")
```

---

## 4. 💰 Prijs calculator *(Medium)*

Voeg prijzen toe per verf en bereken het totaal van de bestellijst. Handig om te weten hoeveel het gaat kosten.

**Waar:** Nieuwe kolom in inventory.csv met prijzen, en totaal in Bestellijst tab

**Stappen:**
1. Voeg een `prijs` kolom toe aan `data/inventory.csv`
2. Voeg prijzen toe per verf (bijv. Model Air = €3.50, Model Color = €3.20, etc.)
3. In de bestellijst, bereken het totaal:

```python
totaal = sum(p['tekort'] * p['prijs'] for p in must_buy)
st.write(f"### 💰 Totaal: €{totaal:.2f}")
```

---

## 5. ✏️ Voorraad aanpassen in de app *(Moeilijk)*

Laat papa aantallen veranderen in de app (bijv. als hij een potje leeg heeft) en sla het op naar de CSV.

**Waar:** Nieuw menu-item "Voorraad bewerken"

**Stappen:**
1. Toon alle verven in een bewerkbare tabel (`st.data_editor`)
2. Bij klik op "Opslaan", schrijf de nieuwe data naar `inventory.csv`
3. Herlaad de voorraad

```python
if keuze == "Voorraad bewerken":
    df = pd.DataFrame(paints)
    edited_df = st.data_editor(df)
    if st.button("Opslaan"):
        edited_df.to_csv(INVENTORY_CSV, index=False)
        st.info("✅ Voorraad opgeslagen!")
```

---

## 6. 📦 Kant-en-klare projecten *(Moeilijk)*

Maak alvast CSV bestanden voor populaire model kits met de juiste kleuren erin. Papa kiest gewoon een model en ziet meteen wat hij nodig heeft.

**Waar:** `projects/` map

**Voorbeeld - Panzer IV (denkbeeldig):**
```csv
kleurnaam,reeks,volledig_nummer,aantal_nodig
Model Air - Dark Yellow,Model Air,71.025,2
Model Air - Olive Green,Model Air,71.007,1
Model Air - Red Brown,Model Air,71.043,1
```

**Ideaal:** Kijk in de bouwdoos van het model welke kleuren aanbevolen worden en maak daar een CSV van.

---

## Prioriteit

| # | Feature | Moeilijkheid | Nut voor papa |
|---|---------|-------------|---------------|
| 1 | Lage voorraad waarschuwing | ★☆☆ | ⭐⭐⭐ |
| 2 | Grafiek per reeks | ★☆☆ | ⭐⭐ |
| 3 | Print-vriendelijke bestellijst | ★☆☆ | ⭐⭐⭐ |
| 4 | Prijs calculator | ★★☆ | ⭐⭐⭐ |
| 5 | Voorraad aanpassen in app | ★★★ | ⭐⭐⭐ |
| 6 | Kant-en-klare projecten | ★★☆ | ⭐⭐⭐ |
