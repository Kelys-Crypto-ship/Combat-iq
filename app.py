import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Combat IQ - AI Edition", layout="wide")

# --- STYLE PERSONNALISÉ (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #d62728; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION DES DONNÉES (SESSION STATE) ---
if 'xp' not in st.session_state:
    st.session_state.xp = 0
    st.session_state.perf = {"Force": 1.2, "Cardio": 2200, "Reaction": 25, "Detente": 45}
    st.session_state.done_days = []
    st.session_state.sport = "MMA"

# --- LOGIQUE RPG ---
level = int(math.sqrt(st.session_state.xp / 100)) + 1
grades = [(81, "🔥 LÉGENDE"), (51, "🔴 ÉLITE"), (31, "🟣 PRO"), (16, "🔵 ESPOIR"), (0, "⚪ NOVICE")]
current_grade = next(g for l, g in grades if level >= l)

# --- SIDEBAR (PROFIL & XP) ---
with st.sidebar:
    st.title("🥊 COMBAT IQ")
    st.metric("NIVEAU", level)
    st.caption(f"Grade : {current_grade}")
    st.progress(min((st.session_state.xp % 100) / 100, 1.0))
    st.write(f"XP Totale : {st.session_state.xp}")
    
    st.divider()
    st.session_state.sport = st.selectbox("Discipline", ["MMA", "Football", "Basketball", "Crossfit"])
    weight = st.number_input("Ton Poids (kg)", value=75)

# --- TABS PRINCIPALES ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 STATS", "🏋️ ENTRAÎNEMENT", "🤖 COACH IA", "📖 GUIDE"])

# --- TAB 1 : STATS & RADAR ---
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Tes Records")
        f = st.number_input("Squat Max (kg)", value=80)
        c = st.number_input("Cooper (mètres)", value=2200)
        r = st.number_input("Réaction (cm)", value=25)
        d = st.number_input("Détente (cm)", value=45)
        
        if st.button("Mettre à jour les Stats (+500 XP)"):
            st.session_state.perf = {"Force": f/weight, "Cardio": c, "Reaction": r, "Detente": d}
            st.session_state.xp += 500
            st.success("Stats synchronisées !")

    with col2:
        # Graphique Radar avec Plotly (plus beau sur mobile)
        categories = ['Force', 'Cardio', 'Réaction', 'Détente']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[st.session_state.perf["Force"]*40, st.session_state.perf["Cardio"]/40, 100-(st.session_state.perf["Reaction"]*2), st.session_state.perf["Detente"]],
            theta=categories, fill='toself', name='Toi', fillcolor='rgba(214, 39, 40, 0.5)', line=dict(color='#d62728')
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2 : ENTRAÎNEMENT (300J) ---
with tab2:
    st.subheader("Programme Odyssey")
    cycle = ["HAUT", "BAS", "CARDIO", "HAUT", "BAS", "CORE", "RECUP", "DETENTE", "HAUT", "BAS", "CARDIO", "EXPLOSION", "TECHNIQUE", "CORE", "RECUP"]
    
    cols = st.columns(5)
    for i in range(1, 31): # Affichage des 30 premiers jours pour l'exemple
        with cols[(i-1)%5]:
            day_type = cycle[(i-1)%15]
            if i in st.session_state.done_days:
                st.button(f"J{i} ✅", key=f"d{i}", disabled=True)
            else:
                if st.button(f"J{i}\n{day_type}", key=f"d{i}"):
                    st.session_state.done_days.append(i)
                    st.session_state.xp += 100
                    st.rerun()

# --- TAB 3 : COACH IA (CERVEAU) ---
with tab3:
    st.subheader("🤖 Ton Coach Stratégique")
    st.info("L'IA analyse tes performances actuelles pour optimiser ta progression.")
    
    # Simulation de l'analyse IA (Peut être remplacé par un appel API)
    if st.button("Demander une analyse au Coach"):
        with st.spinner("Le coach examine tes données..."):
            # Ici on simule une réponse intelligente basée sur les stats
            if st.session_state.perf["Cardio"] < 2500:
                conseil = "Ton endurance est ton maillon faible actuel. Je te suggère d'ajouter 15 min de corde à sauter à la fin de chaque séance."
            else:
                conseil = "Ton cardio est solide. On va se concentrer sur ta puissance de frappe (Force Relative)."
            
            st.chat_message("assistant").write(f"Salut Athlète ! Voici mon analyse : {conseil}")
            st.chat_message("assistant").write(f"Prochain objectif : Atteindre le niveau {level + 1} pour débloquer le prochain Boss.")

# --- TAB 4 : GUIDE ---
with tab4:
    st.write("### Protocoles officiels")
    with st.expander("Test de Réaction"):
        st.write("Lâche une règle de 30cm... (voir détails dans le guide)")