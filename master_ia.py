import streamlit as st
import datetime

st.set_page_config(page_title="Master IA")
st.title("🎓 MASTER IA : Savoir")

goal = st.text_input("Objectif actuel", "Bac de Français 2026")
date_examen = st.date_input("Date de l'examen", datetime.date(2026, 6, 15))

jours_restants = (date_examen - datetime.date.today()).days
st.metric("Jours restants", jours_restants)

st.write("### Modules à valider")
modules = ["Analyse de texte", "Grammaire", "Littérature"]
for m in modules:
    col_m, col_b = st.columns([4, 1])
    col_m.write(m)
    if col_b.button("Valider", key=m):
        st.balloons()
