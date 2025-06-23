import streamlit as st
import re
import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

# 🔐 .env-Datei laden (optional, falls vorhanden)
load_dotenv()

# 💰 Token-Kosten GPT-3.5 (geschätzt pro 1000 Tokens)
COST_INPUT = 0.0005
COST_OUTPUT = 0.0015

# 📧 Titel anzeigen
st.title("📧 NRC Anfrage-zu-Antwort Generator mit GPT")

# 📂 API-Key aus Umgebungsvariable laden
api_key_input = os.getenv("OPENAI_API_KEY")
if not api_key_input:
    st.error("❌ Kein API-Key gefunden. Bitte stellen Sie sicher, dass eine .env-Datei mit OPENAI_API_KEY vorhanden ist.")
    st.stop()

client = OpenAI(api_key=api_key_input)

# 🧠 Kundenanfrage analysieren
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

# 📧 GPT-generierte Mail erstellen + Kosten schätzen
def generate_gpt_email(anrede, nachname, geraet, problem, reparaturart, preis, dauer):
    prompt = f"""
Formuliere eine professionelle und freundliche Antwort-E-Mail im Namen eines Reparaturservices an eine(n) Kund:in namens {anrede} {nachname}. Die Person hat ein Problem mit folgendem Gerät: {geraet}.

Fehlerbeschreibung:
{problem}

Bitte erwähne, dass die Reparatur möglich ist. Der Preis für die Reparaturart \"{reparaturart}\" beträgt {preis} € und die Bearbeitungsdauer beträgt ca. {dauer}. Verwende einen respektvollen und kompetenten Ton und hänge folgenden Abschlussteil an:

Wir untersuchen kostenlos Ihr Gerät und erstellen anschließend eine professionelle Diagnose sowie den kostenlosen Kostenvoranschlag.
 
Sie haben folgende Möglichkeiten, um uns das Gerät zu übermitteln: 

1. Bringen Sie das Gerät zu einer unserer Annahmestationen Graz, Linz, Wien und München, wo eine Mitarbeiterin oder ein Mitarbeiter das Gerät entgegennimmt, mit Ihnen das Reparaturformular ausfüllt und sich um die professionelle Weiterleitung an unsere Technikabteilungen und Zentrale nach Salzburg (Kunden aus Österreich) oder Freilassing (Kunden aus Deutschland) kümmert.

2. Versenden Sie es direkt in die NRC Salzburg, Kaiserschützenstraße 8, 5020 Salzburg, Österreich oder für die Kunden aus Deutschland an die NRC Repair GmbH, Münchener Straße 8, 83395 Freilassing, Deutschland. Bitte drucken Sie dazu von unserer Homepage das Reparaturformular aus und legen Sie es ausgefüllt dem Gerät bei.

Mit freundlichen Grüßen
Ihr NRC Technikteam
https://notebook-repair-corner.at
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        completion = response.choices[0].message.content.strip()
        usage = response.usage
        cost_estimate = (usage.prompt_tokens * COST_INPUT + usage.completion_tokens * COST_OUTPUT)
        return completion, cost_estimate
    except OpenAIError as e:
        return f"❌ Fehler bei der GPT-Anfrage: {str(e)}", 0.0

# 🔍 Verbindungstest
if st.button("🔍 API-Verbindung testen"):
    try:
        client.models.list()
        st.success("✅ Verbindung erfolgreich hergestellt.")
    except Exception as e:
        st.error(f"❌ Verbindung fehlgeschlagen: {str(e)}")

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

    if st.button("🤖 GPT-E-Mail generieren"):
        with st.spinner("ChatGPT denkt nach..."):
            mail, kosten = generate_gpt_email(anrede, nachname, geraet, problem, reparaturart, preis, dauer)
        st.text_area("📄 Generierte GPT-E-Mail", mail, height=600)
        st.markdown(f"💰 **Geschätzte GPT-Kosten:** {kosten:.4f} USD")

    if st.button("📄 Standard-E-Mail (fixer Text)"):
        mail = f"""
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
        st.text_area("📄 Generierte Standard-E-Mail", mail.strip(), height=600)
