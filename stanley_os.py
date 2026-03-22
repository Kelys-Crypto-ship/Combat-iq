import streamlit as st
import pandas as pd
import datetime
import google.generativeai as genai
import plotly.express as px

st.set_page_config(page_title="STANLEY OS", layout="wide")

# --- FONCTION VOIX NATIVE ---
def stanley_parle(texte):
    js_code = f"""<script>var msg = new SpeechSynthesisUtterance("{texte}");msg.lang = 'fr-FR';msg.pitch = 0.8;window.speechSynthesis.speak(msg);</script>"""
    st.components.v1.html(js_code, height=0)

# --- BASE DE DONNÉES SIMULÉE ---
if 'stats' not in st.session_state:
    st.session_state.stats = {"Discipline": 50, "Combat": 30, "Savoir": 20}
    st.session_state.tasks = [
        {"heure": "08:00", "tache": "Briefing Stanley", "done": False},
        {"heure": "09:00", "tache": "Entraînement Combat IQ", "done": False},
        {"heure": "14:00", "tache": "Module Master IA", "done": False}
    ]

# --- INTERFACE ---
st.title("🕴️ STANLEY : Système Maître")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📅 Planning Dynamique")
    for i, t in enumerate(st.session_state.tasks):
        c1, c2, c3 = st.columns([1, 4, 1])
        c1.write(t['heure'])
        c2.write(f"**{t['tache']}**")
        if c3.button("OK", key=f"t_{i}"):
            st.session_state.tasks[i]['done'] = True
            st.session_state.stats["Discipline"] += 5
            st.rerun()

with col2:
    st.subheader("📊 État du Sujet")
    df = pd.DataFrame(dict(r=list(st.session_state.stats.values()), theta=list(st.session_state.stats.keys())))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself', line_color='#ff4b4b')
    st.plotly_chart(fig, use_container_width=True)

if st.button("🔊 LANCER LE BRIEFING VOCAL"):
    msg = f"Bonjour. Ta discipline est à {st.session_state.stats['Discipline']}%. "
    if st.session_state.stats['Savoir'] < 30:
        msg += "Ton niveau de savoir est critique. Stanley exige une session Master IA aujourd'hui."
    stanley_parle(msg)
