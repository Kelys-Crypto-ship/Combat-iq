import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
import google.generativeai as genai

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Combat IQ - AI Edition", layout="wide", initial_sidebar_state="expanded")

# --- STYLE CSS (DARK MODE & BOUTONS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #d62728; color: white; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #ff3131; border: 1px solid white; }
    [data-testid="stMetricValue"] { color: #f1c40f; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION DES DONNÉES ---
if 'xp' not in st.session_state:
    st.session_state.xp = 0
    st.session_state.perf = {"Force": 1.0, "Cardio": 2000, "Reaction": 30, "Detente": 40}
    st.session_state.done_days = []
    st.session_state.sport = "MMA"
    st.session_state.weight = 75

# --- LOGIQUE RPG ---
level = int(math.sqrt(st.session_state.xp / 100)) + 1
grades = [(81, "🔥 LÉGENDE"), (51, "🔴 ÉLITE"), (31, "🟣 PRO"), (16, "🔵 ESPOIR"), (0, "⚪ NOVICE")]
current_grade = next(g for l, g in grades if level >= l)

# --- CONFIGURATION IA (GEMINI) ---
ai_ready = False
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
        ai_ready = True
    except:
        ai_ready = False

# --- SIDEBAR ---
with st.sidebar:
    st.title("🥊 COMBAT IQ")
    st.subheader(f"Statut : {current_grade}")
    st.metric("NIVEAU", level)
    
    # Barre de progression XP
    xp_current_lvl = (level - 1)**2 * 100
    xp_next_lvl = level**2 * 100
    progress = (st.session_state.xp - xp_current_lvl) / (xp_next_lvl - xp_current_lvl)
    st.progress(min(max(progress, 0.0), 1.0))
    st.caption(f"XP : {st.session_state.xp} / {xp_next_lvl}")
    
    st.divider()
    st.session_state.sport = st.selectbox("Discipline", ["MMA", "Football", "Basketball", "Crossfit", "Boxe"])
    st.session_state.weight = st.number_input("Poids actuel (kg)", value=st.session_state.weight)
    st.info(f"Coach IA : {'✅ Connecté' if ai_ready else '❌ Déconnecté'}")

# --- CORPS DE L'APPLICATION ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 STATS", "🏋️ PROGRAMME", "👹 BOSS", "🤖 COACH IA", "📖 GUIDE"])

# --- TAB 1 : STATS & RADAR ---
with tab1:
    st.header("Analyse de Performance")
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.write("### Tes Records (T0)")
        f_val = st.number_input("Squat Max (kg)", value=80)
        c_val = st.number_input("Cooper (mètres)", value=2200)
        r_val = st.number_input("Réaction (cm)", value=25)
        d_val = st.number_input("Détente (cm)", value=45)
        
        if st.button("SAUVEGARDER & GAGNER 500 XP"):
            st.session_state.perf = {"Force": f_val/st.session_state.weight, "Cardio": c_val, "Reaction": r_val, "Detente": d_val}
            st.session_state.xp += 500
            st.rerun()

    with col2:
        # Données Pro/WR simplifiées pour le radar
        categories = ['Force (Rel)', 'Cardio', 'Réaction (Inv)', 'Détente']
        # Normalisation des scores pour le radar (0-100)
        user_scores = [
            min(100, (st.session_state.perf["Force"]/2.5)*100),
            min(100, (st.session_state.perf["Cardio"]/3600)*100),
            min(100, (10/st.session_state.perf["Reaction"])*100 if st.session_state.perf["Reaction"] > 0 else 0),
            min(100, (st.session_state.perf["Detente"]/100)*100)
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=user_scores, theta=categories, fill='toself', name='Toi', fillcolor='rgba(214, 39, 40, 0.4)', line=dict(color='#d62728')))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="gray")), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2 : ENTRAÎNEMENT (300J) ---
with tab2:
    st.header("Odyssée des 300 Jours")
    cycle = ["HAUT", "BAS", "CARDIO", "HAUT", "BAS", "CORE", "RECUP", "DETENTE", "HAUT", "BAS", "CARDIO", "EXPLOSION", "TECHNIQUE", "CORE", "RECUP"]
    
    # Affichage en grille responsive
    n_cols = 5
    rows = st.columns(n_cols)
    for i in range(1, 31): # Aperçu du mois actuel
        with rows[(i-1)%n_cols]:
            day_type = cycle[(i-1)%15]
            if i in st.session_state.done_days:
                st.write(f"J{i} ✅")
            else:
                if st.button(f"J{i}\n{day_type}", key=f"btn_j{i}"):
                    st.session_state.done_days.append(i)
                    st.session_state.xp += 100
                    st.rerun()

# --- TAB 3 : BOSS ---
with tab3:
    st.header("Arène des Boss")
    boss_names = ["L'Ombre", "Le Garde", "Le Capitaine", "L'Elite", "Le Titan", "Le Colosse"]
    b_cols = st.columns(3)
    for idx, name in enumerate(boss_names):
        with b_cols[idx % 3]:
            locked = len(st.session_state.done_days) < (idx + 1) * 30
            if locked:
                st.button(f"BOSS {idx+1}\n🔒 BLOQUÉ", key=f"b{idx}", disabled=True)
            else:
                if st.button(f"COMBATTRE\n{name}", key=f"b{idx}"):
                    st.balloons()
                    st.session_state.xp += 1000
                    st.success(f"Boss {name} vaincu ! +1000 XP")

# --- TAB 4 : COACH IA ---
with tab3 if not ai_ready else tab4:
    st.header("🤖 Coach Stratégique Personnel")
    if not ai_ready:
        st.warning("Connecte ta clé API Gemini dans les Secrets pour activer le coach.")
    else:
        if st.button("Lancer un Diagnostic de Performance"):
            prompt = f"""Tu es un coach expert en {st.session_state.sport}. 
            L'athlète a ces stats : Force {st.session_state.perf['Force']}x son poids, 
            Cardio {st.session_state.perf['Cardio']}m au Cooper, 
            Réaction {st.session_state.perf['Reaction']}cm, 
            Détente {st.session_state.perf['Detente']}cm. 
            Donne un avis bref, motivant et 3 axes d'amélioration précis."""
            
            with st.spinner("Analyse en cours..."):
                try:
                    response = model.generate_content(prompt)
                    st.chat_message("assistant").write(response.text)
                except Exception as e:
                    st.error("Erreur de connexion avec l'IA.")

# --- TAB 5 : GUIDE MÉTHODES ---
with tab5:
    st.header("Guide des Protocoles")
    guide_list = {
        "🧠 Réaction (Règle)": "Lâcher une règle de 30cm sans prévenir. La pincer le plus vite possible. Note la distance.",
        "🚀 Détente (Saut)": "Saut vertical pieds joints contre un mur. Mesure la différence entre bras levé et impact saut.",
        "🫁 Cooper (Cardio)": "Distance maximale parcourue en courant pendant exactement 12 minutes.",
        "🏋️ Force (Squat)": "Ton Record personnel (1RM) divisé par ton poids de corps (ex: 1.5x)."
    }
    for title, desc in guide_list.items():
        with st.expander(title):
            st.write(desc)
with tab4:
    st.write("### Protocoles officiels")
    with st.expander("Test de Réaction"):
        st.write("Lâche une règle de 30cm... (voir détails dans le guide)")
