
import streamlit as st
import re

def parse_customer_request(text):
    vorname = re.search(r"Vorname:\s*(.*)", text)
    nachname = re.search(r"Nachname:\s*(.*)", text)
    fehler = re.search(r"Sonstige Fehlerbeschreibung:\s*(.*)", text, re.DOTALL)
    geraet = re.search(r"Gerätetyp:\s*(.*)", text)
    modell = re.search(r"Modellbezeichnung\s*(.*)", text)

    return {
        "vorname": vorname.group(1).strip() if vorname else "",
        "nachname": nachname.group(1).strip() if nachname else "",
        "geraet": modell.group(1).strip() if modell else geraet.group(1).strip() if geraet else "",
        "fehler": fehler.group(1).strip() if fehler else ""
    }

def generate_email(anrede, nachname, geraet, problem, reparaturart, preis, dauer):
    return f"""Betreff: Ihre Anfrage zur {geraet}

Sehr geehrte{anrede} {nachname},

vielen Dank für Ihre Anfrage und die genaue Fehlerbeschreibung.

Nach Ihrer Schilderung handelt es sich sehr wahrscheinlich um {problem}. Diese Reparatur können wir selbstverständlich für Sie durchführen.

✅ Der Preis für {reparaturart} beträgt **{preis} €**  
🕒 Die Reparaturdauer beträgt ca. **{dauer}** nach Geräteeingang.

Wir untersuchen kostenlos Ihr Gerät und erstellen anschließend eine professionelle Diagnose sowie den kostenlosen Kostenvoranschlag.

Sie haben folgende Möglichkeiten, um uns das Gerät zu übermitteln:

1. Bringen Sie das Gerät zu einer unserer Annahmestationen Graz, Linz, Wien und München, wo eine Mitarbeiterin oder ein Mitarbeiter das Gerät entgegennimmt, mit Ihnen das Reparaturformular ausfüllt und sich um die professionelle Weiterleitung an unsere Technikabteilungen und Zentrale nach Salzburg (Kunden aus Österreich) oder Freilassing (Kunden aus Deutschland) kümmert.

2. Versenden Sie es direkt in die NRC Salzburg, Kaiserschützenstraße 8, 5020 Salzburg, Österreich oder für die Kunden aus Deutschland an die NRC Repair GmbH, Münchener Straße 8, 83395 Freilassing, Deutschland. Bitte drucken Sie dazu von unserer Homepage das Reparaturformular aus und legen Sie es ausgefüllt dem Gerät bei.

Mit freundlichen Grüßen  
Ihr NRC Technikteam  
https://notebook-repair-corner.at
"""

st.title("📧 NRC Anfrage-zu-Antwort Generator")

kundenanfrage = st.text_area("📝 Kundenanfrage einfügen", height=300)

if kundenanfrage:
    daten = parse_customer_request(kundenanfrage)
    anrede = " Frau" if daten['vorname'] and daten['vorname'].strip()[-1].lower() == 'e' else " Herr"
    nachname = daten['nachname']
    geraet = daten['geraet']
    problem = daten['fehler']

    st.markdown("---")
    st.subheader("📌 Reparaturdetails ergänzen")
    reparaturart = st.text_input("Reparaturart", value="Reparatur der Ladebuchse")
    preis = st.text_input("Preis (€)", value="119")
    dauer = st.text_input("Dauer", value="5–7 Werktage")

    if st.button("📨 E-Mail generieren"):
        mail = generate_email(anrede, nachname, geraet, problem, reparaturart, preis, dauer)
        st.text_area("📄 Generierte E-Mail", mail, height=600)
