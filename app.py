import streamlit as st

st.set_page_config(page_title="Combat IQ")
st.title("🥊 COMBAT IQ : Performance")

# Système de Grades
grades = ["Novice", "Initié", "Soldat", "Guerrier", "Légende"]
xp = st.slider("Ton XP de Combat", 0, 1000, 150)
grade_actuel = grades[xp // 200]

st.metric("Grade Actuel", grade_actuel)
st.progress(xp % 200 / 200)

st.subheader("Séance du jour : Force & Réactivité")
if st.button("Valider l'entraînement (+50 XP)"):
    st.success("Bravo ! Stanley a été notifié de ta progression physique.")
    st.write("### Protocoles officiels")
    with st.expander("Test de Réaction"):
        st.write("Lâche une règle de 30cm... (voir détails dans le guide)")
