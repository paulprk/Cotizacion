import streamlit as st
from datetime import datetime, timedelta
import urllib.parse

# ==========================================
# CONFIGURACIÓN DE TASA (MODIFICA AQUÍ)
# ==========================================
COTIZACION_OFICIAL = 1435  # <-- Cambia este número cuando suba o baje el dólar
# ==========================================

# 1. Configuración de página
st.set_page_config(page_title="Arqui Giros - Oficial", page_icon="💸")

# Estilo visual
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stRadio > div { flex-direction: row; justify-content: center; }
    /* Estilo para el botón de Calcular */
    div.stButton > button:first-child {
        background-color: #1e3799;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    /* Estilo para el botón de WhatsApp */
    .whatsapp-button {
        background-color: #25D366;
        color: white;
        padding: 18px;
        text-align: center;
        border-radius: 12px;
        font-weight: bold;
        font-size: 20px;
        text-decoration: none;
        display: block;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Cálculo de HORA ARGENTINA (GMT-3)
ahora_arg = datetime.utcnow() - timedelta(hours=3)
ahora = ahora_arg.strftime("%d/%m/%Y %H:%M")

# 3. Encabezado
col_logo1, col_logo2, col_logo3 = st.columns([1,2,1])
with col_logo2:
    try:
        st.image("logo.png", width=200)
    except:
        st.markdown("<h1 style='text-align: center; color: #1e3799;'>🏦 ARQUI GIROS</h1>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center; font-size: 20px;'><b>Cotización del día:</b> 1 USD = {COTIZACION_OFICIAL:,} ARS</p>".replace(",", "."), unsafe_allow_html=True)
st.divider()

# 4. Entradas de datos optimizadas
col1, col2 = st.columns(2)

with col1:
    opciones_montos = ["50.00", "100.00", "200.00", "300.00", "400.00", "Otro monto..."]
    seleccion = st.selectbox("Monto en USD:", opciones_montos, index=1)

    if seleccion == "Otro monto...":
        dol = st.number_input("Ingrese monto manual:", min_value=0.0, step=1
