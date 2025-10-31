import streamlit as st
from main import *  # Importar les funcions de main.py

st.set_page_config(page_title="⚽ WaterPolo Manager", page_icon="🤽", layout="wide")

st.title("🤽 WaterPolo Match Simulator")
st.markdown("---")

# Sidebar amb configuració
st.sidebar.header("⚙️ Match Configuration")

# Botons per iniciar simulació
if st.sidebar.button("🎮 Start New Match", type="primary"):
    with st.spinner("Simulating match..."):
        # Aquí crides les funcions del main.py per simular el partit
        # Necessitaràs adaptar el codi segons com funcioni main.py
        
        st.success("✅ Match simulation completed!")

# Mostrar resultats
st.header("📊 Match Results")
# Aquí mostraràs els resultats de la simulació
