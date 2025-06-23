
import streamlit as st

def generate_email(anrede, nachname, geraet, problem, reparaturart, preis, dauer):
    return f"""
Betreff: Ihre Anfrage zur {geraet}

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

# Streamlit UI
st.title("📧 NRC Antwortgenerator")

anrede = st.selectbox("Anrede", [" Frau", " Herr"])
nachname = st.text_input("Nachname")
geraet = st.text_input("Gerätetyp / Problem")
problem = st.text_area("Kurze Problembeschreibung")
reparaturart = st.text_input("Reparaturart")
preis = st.text_input("Preis (€)")
dauer = st.text_input("Dauer")

if st.button("📨 E-Mail generieren"):
    email = generate_email(anrede, nachname, geraet, problem, reparaturart, preis, dauer)
    st.text_area("📄 Generierte E-Mail", email, height=600)
