import streamlit as st
from datetime import datetime, timedelta
import urllib.parse

# 1. Configuración de página
st.set_page_config(page_title="Recibo Cambio - AR", page_icon="💸")

# --- ESPACIO PARA EL LOGO ---
# Si subes tu logo a GitHub, quita el '#' de la línea de abajo y pon el nombre de tu archivo
# st.image("logo.png", width=200) 

# Estilo visual para mejorar la apariencia en móviles
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stRadio > div { flex-direction: row; justify-content: center; }
    div.stButton > button:first-child {
        background-color: #25D366;
        color: white;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar - Control de Tasa (Para que lo actualices tú)
with st.sidebar:
    st.header("⚙️ Configuración Admin")
    tasa_actualizada = st.number_input("Tasa USD/ARS:", value=1435, step=1)
    st.divider()
    st.caption("Actualiza aquí el valor del dólar cada día.")

# 3. Cálculo de HORA ARGENTINA (GMT-3) sin librerías extras
ahora_arg = datetime.utcnow() - timedelta(hours=3)
ahora = ahora_arg.strftime("%d/%m/%Y %H:%M")

# 4. Interfaz Principal
st.markdown("<h1 style='text-align: center; color: #1e3799;'>🏦 RECIBO CAMBIO</h1>", unsafe_allow_html=True)
st.write(f"💹 **Cotización:** 1 USD = {tasa_actualizada:,} ARS".replace(",", "."))
st.write(f"📅 **Fecha:** {ahora}")
st.divider()

# 5. Entradas de datos
col1, col2 = st.columns(2)
with col1:
    dol = st.number_input("Monto en USD:", min_value=0.0, step=1.0, format="%.2f")
with col2:
    comision_sel = st.radio("¿Comisión?", ["Incluida", "Aparte"])

# 6. Lógica de cálculo (Tu código original)
MENOS_60 = 1.5
MAS_60 = 0.025

if dol > 0:
    if dol <= 60:
        com_final = MENOS_60
    else:
        com_final = int(dol * MAS_60 * 100) / 100

    if comision_sel == "Incluida":
        monto_recibir_ars = (dol - com_final) * tasa_actualizada
        monto_transferir_usd = dol
        txt_com = f"{com_final:.2f} USD (Deducida)"
    else:
        monto_recibir_ars = dol * tasa_actualizada
        monto_transferir_usd = dol + com_final
        txt_com = f"{com_final:.2f} USD (Aparte)"

    # Función para formatear números (Ej: 1.000,00)
    def fmt(n):
        return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # 7. Cuadro de Resultado Visual
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 5px solid #2ecc71; color: black; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);">
        <p style="margin:5px 0;"><b>Monto:</b> {fmt(dol)} USD</p>
        <p style="margin:5px 0;"><b>Comisión:</b> {txt_com}</p>
        <hr>
        <h2 style="color: #27ae60; margin:10px 0;">RECIBIR: {fmt(monto_recibir_ars)} ARS</h2>
        <h2 style="color: #e67e22; margin:0;">TRANSFERIR: {fmt(monto_transferir_usd)} USD</h2>
    </div>
    """, unsafe_allow_html=True)

    # 8. Botón de Compartir (Universal para todo el equipo)
    mensaje = (
        f"*RECIBO CAMBIO*\n"
        f"------------------------------\n"
        f"📅 *Fecha:* {ahora}\n"
        f"💵 *Monto:* {fmt(dol)} USD\n"
        f"⚙️ *Comisión:* {txt_com}\n\n"
        f"💰 *RECIBIR: {fmt(monto_recibir_ars)} ARS*\n"
        f"💳 *TRANSFERIR: {fmt(monto_transferir_usd)} USD*\n"
        f"------------------------------\n"
        f"Cotización: 1 USD = {fmt(tasa_actualizada).replace(',00','')}"
    )
    
    msg_encoded = urllib.parse.quote(mensaje)
    share_url = f"https://api.whatsapp.com/send?text={msg_encoded}"

    st.write("")
    st.markdown(f'''
        <a href="{share_url}" target="_blank" style="text-decoration: none;">
            <div style="width:100%; background-color:#25D366; color:white; padding:18px; text-align:center; border-radius:12px; font-weight:bold; font-size:20px; box-shadow: 0px 4px 10px rgba(0,0,0,0.15);">
                🟢 COMPARTIR POR WHATSAPP
            </div>
        </a>
    ''', unsafe_allow_html=True)

st.divider()
st.caption("AL REALIZAR UN GIRO SE DA POR LEÍDO LOS T&C")
