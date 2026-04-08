import streamlit as st
from datetime import datetime, timedelta
import urllib.parse
import base64
import os

# ==========================================
# CONFIGURACIÓN DE TASA (MODIFICA AQUÍ)
# ==========================================
COTIZACION_OFICIAL = 1445
# ==========================================

st.set_page_config(page_title="Arqui Giros - Oficial", page_icon="💸")

# --- FUNCIÓN PARA CARGAR IMAGEN ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

img_name = "Gemini_Generated_Image_pz70wopz70wopz70.png"
img_base64 = get_base64_image(img_name)

# Estilos CSS
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stRadio > div { flex-direction: row; justify-content: center; }
    
    .arqui-title {
        text-align: center; color: #1e3799; font-weight: bold; font-size: 30px;
        display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 5px;
    }
    .title-logo { height: 30px; width: auto; }

    .cotizacion-box {
        text-align: center; width: 100%; font-size: 18px; font-weight: bold;
        color: #31333F; margin-bottom: 10px;
    }

    div.stButton > button:first-child {
        background-color: #1e3799; color: white; border-radius: 8px;
        height: 3em; width: 100%; font-weight: bold;
    }

    .whatsapp-link { text-decoration: none; display: flex; justify-content: center; margin-top: 10px; }
    .btn-ws {
        display: flex; align-items: center; justify-content: center; gap: 8px;
        padding: 12px 15px; border-radius: 6px; font-weight: 600; font-size: 14px;
        color: white !important; width: fit-content; min-width: 200px;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.1);
    }
    .bg-active { background-color: #25D366; }
    .bg-inactive { background-color: #e0e0e0; color: #888888 !important; pointer-events: none; }
    .ws-icon { height: 16px; width: auto; }
    
    input { text-align: center; }
    .comision-info { text-align: center; font-size: 12px; color: #666; margin-top: -10px; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
title_html = '<div class="arqui-title">'
if img_base64: title_html += f'<img src="data:image/png;base64,{img_base64}" class="title-logo">'
else: title_html += '🏦 '
title_html += 'Arqui Giros</div>'
st.markdown(title_html, unsafe_allow_html=True)
st.markdown(f'<div class="cotizacion-box">Cotización: 1 USD = {COTIZACION_OFICIAL:,} ARS</div>'.replace(",", "."), unsafe_allow_html=True)

# NUEVO: Selector de Modo
st.markdown("---")
opcion_giro = st.selectbox("¿Qué operación desea realizar?", 
                         ["💵 Dólares a Pesos (Recibir en AR)", "🇦🇷 Pesos a Dólares (Recibir en USD)"])

if 'calc_step' not in st.session_state:
    st.session_state.calc_step = False

# PASO 1: ENTRADA DINÁMICA
col1, col2 = st.columns(2)
with col1:
    label_monto = "Monto en USD:" if "Dólares a Pesos" in opcion_giro else "Monto en ARS:"
    monto_texto = st.text_input(label_monto, value="100.00", disabled=st.session_state.calc_step)
    try: monto_usr = float(monto_texto.replace(",", "."))
    except ValueError: monto_usr = 0.0

with col2:
    comision_sel = st.radio("Comisión", ["Incluida", "Aparte"], disabled=st.session_state.calc_step)
    text_com_help = "Se descuenta del total" if comision_sel == "Incluida" else "Se suma al total"
    st.markdown(f'<p class="comision-info">{text_com_help}</p>', unsafe_allow_html=True)

if not st.session_state.calc_step:
    if st.button("🚀 CALCULAR COTIZACIÓN"):
        if monto_usr > 0:
            st.session_state.calc_step = True
            st.rerun()

# PASO 2: CÁLCULOS DINÁMICOS
if st.session_state.calc_step:
    # 1. Calculamos los valores base según el sentido
    if "Dólares a Pesos" in opcion_giro:
        usd_base = monto_usr
        com_final = 1.5 if usd_base <= 60 else int(usd_base * 0.025 * 100) / 100
        if comision_sel == "Incluida":
            recibir = round((usd_base - com_final) * COTIZACION_OFICIAL)
            transferir = usd_base
            txt_res = f"RECIBIR: {recibir:,} ARS".replace(",", ".")
            txt_det = f"Monto: {usd_base:.2f} USD | Comisión: {com_final:.2f} USD"
            txt_tra = f"Transferir: {usd_base:.2f} USD"
        else:
            recibir = round(usd_base * COTIZACION_OFICIAL)
            transferir = usd_base + com_final
            txt_res = f"RECIBIR: {recibir:,} ARS".replace(",", ".")
            txt_det = f"Monto: {usd_base:.2f} USD | Comisión: {com_final:.2f} USD"
            txt_tra = f"Transferir: {transferir:.2f} USD"
    else:
        # Lógica Pesos a Dólares
        ars_base = monto_usr
        usd_equivalente = ars_base / COTIZACION_OFICIAL
        com_final = 1.5 if usd_equivalente <= 60 else int(usd_equivalente * 0.025 * 100) / 100
        
        if comision_sel == "Incluida":
            recibir_usd = usd_equivalente - com_final
            transferir_ars = ars_base
            txt_res = f"RECIBIR: {recibir_usd:.2f} USD"
            txt_det = f"Monto: {ars_base:,} ARS | Comisión: {com_final:.2f} USD".replace(",", ".")
            txt_tra = f"Transferir: {ars_base:,} ARS".replace(",", ".")
        else:
            recibir_usd = usd_equivalente
            transferir_ars = ars_base + (com_final * COTIZACION_OFICIAL)
            txt_res = f"RECIBIR: {recibir_usd:.2f} USD"
            txt_det = f"Monto: {ars_base:,} ARS | Comisión: {com_final:.2f} USD".replace(",", ".")
            txt_tra = f"Transferir: {round(transferir_ars):,} ARS".replace(",", ".")

    # Mostrar Resultado
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 12px; border-left: 5px solid #2ecc71; color: black; margin-bottom: 20px; text-align:center;">
        <h2 style="color: #27ae60; margin:0;">{txt_res}</h2>
        <p style="margin:5px 0; font-size:14px;">{txt_det}</p>
        <p style="color: #e67e22; margin:0; font-weight:bold;">{txt_tra}</p>
    </div>
    """, unsafe_allow_html=True)

    # Datos de destino (se mantienen igual)
    st.markdown("### 📝 Datos de Destino")
    banco_sel = st.selectbox("Banco remitente:", ["Banco Pichincha", "Banco Guayaquil", "Banco Pacífico", "Otro"])
    banco_final = f"Banco {st.text_input('Especifique:')}" if banco_sel == "Otro" else banco_sel
    c1, c2 = st.columns(2)
    with c1: cvu = st.text_input("CBU/CVU o Alias:")
    with c2: nombre = st.text_input("Nombre y Apellido:")

    # WhatsApp Mensaje Dinámico
    ws_icon_url = "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg"
    msg_txt = f"Hola, cotización Arqui Giros ({opcion_giro}):\n\n*Resultado:* {txt_res}\n*Banco:* {banco_final}\n*Destino:* {nombre.upper()}\n*CBU:* {cvu}"
    msg = urllib.parse.quote(msg_txt)
    
    if cvu and nombre:
        st.markdown(f'<div class="whatsapp-link"><a href="https://api.whatsapp.com/send?text={msg}" target="_blank" class="btn-ws bg-active"><img src="{ws_icon_url}" class="ws-icon"> Compartir a WhatsApp</a></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="whatsapp-link" style="flex-direction: column; align-items: center;"><div class="btn-ws bg-inactive"><img src="{ws_icon_url}" class="ws-icon" style="filter:grayscale(1)"> Compartir a WhatsApp</div><p style="color: #ff4b4b; font-size: 13px; margin-top: 8px; font-weight: bold;">⚠️ Complete los datos para compartir</p></div>', unsafe_allow_html=True)

    if st.button("🔄 NUEVA COTIZACIÓN"):
        st.session_state.calc_step = False
        st.rerun()
