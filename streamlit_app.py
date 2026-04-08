import streamlit as st
from datetime import datetime, timedelta
import urllib.parse

# ==========================================
# CONFIGURACIÓN DE TASA (MODIFICA AQUÍ)
# ==========================================
COTIZACION_OFICIAL = 1445  # <-- Cambia este número cuando suba o baje el dólar
# ==========================================

# 1. Configuración de página
st.set_page_config(page_title="Arqui Giros - Oficial", page_icon="💸")

# Estilo visual
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

# 2. Cálculo de HORA ARGENTINA (GMT-3)
ahora_arg = datetime.utcnow() - timedelta(hours=3)
ahora = ahora_arg.strftime("%d/%m/%Y %H:%M")

# 3. Encabezado con el Logo (Asegúrate de tener logo.png en tu GitHub)
col_logo1, col_logo2, col_logo3 = st.columns([1,2,1])
with col_logo2:
    try:
        st.image("logo.png", width=200)
    except:
        st.markdown("<h1 style='text-align: center; color: #1e3799;'>🏦 ARQUI GIROS</h1>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center; font-size: 20px;'><b>Cotización del día:</b> 1 USD = {COTIZACION_OFICIAL:,} ARS</p>".replace(",", "."), unsafe_allow_html=True)
st.write(f"<p style='text-align: center; color: gray;'>Actualizado: {ahora} (ARG)</p>", unsafe_allow_html=True)
st.divider()

# 4. Entradas de datos (Aquí el usuario SOLO ingresa monto y tipo de comisión)
col1, col2 = st.columns(2)
with col1:
    dol = st.number_input("Monto en USD:", min_value=0.0, step=1.0, format="%.2f")
with col2:
    comision_sel = st.radio("¿Comisión?", ["Incluida", "Aparte"])

# 5. Lógica de cálculo
MENOS_60 = 1.5
MAS_60 = 0.025

if dol > 0:
    if dol <= 60:
        com_final = MENOS_60
    else:
        com_final = int(dol * MAS_60 * 100) / 100

    if comision_sel == "Incluida":
        monto_recibir_ars = (dol - com_final) * COTIZACION_OFICIAL
        monto_transferir_usd = dol
        txt_com = f"{com_final:.2f} USD (Deducida)"
    else:
        monto_recibir_ars = dol * COTIZACION_OFICIAL
        monto_transferir_usd = dol + com_final
        txt_com = f"{com_final:.2f} USD (Aparte)"

    def fmt(n):
        return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # 6. Recibo Visual
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 5px solid #2ecc71; color: black;">
        <p style="margin:5px 0;"><b>Monto:</b> {fmt(dol)} USD</p>
        <p style="margin:5px 0;"><b>Comisión:</b> {txt_com}</p>
        <hr>
        <h2 style="color: #27ae60; margin:10px 0;">RECIBIR: {fmt(monto_recibir_ars)} ARS</h2>
        <h2 style="color: #e67e22; margin:0;">TRANSFERIR: {fmt(monto_transferir_usd)} USD</h2>
    </div>
    """, unsafe_allow_html=True)

    # 7. Mensaje de WhatsApp
    mensaje = (
        f"*ARQUI GIROS*\n"
        f"------------------------------\n"
        f"📅 *Fecha:* {ahora}\n"
        f"💵 *Monto:* {fmt(dol)} USD\n"
        f"⚙️ *Comisión:* {txt_com}\n\n"
        f"💰 *RECIBIR: {fmt(monto_recibir_ars)} ARS*\n"
        f"💳 *TRANSFERIR: {fmt(monto_transferir_usd)} USD*\n"
        f"------------------------------\n"
        f"Tasa aplicada: 1 USD = {fmt(COTIZACION_OFICIAL).replace(',00','')}"
    )
    
    msg_encoded = urllib.parse.quote(mensaje)
    share_url = f"https://api.whatsapp.com/send?text={msg_encoded}"

    st.write("")
    st.markdown(f'''
        <a href="{share_url}" target="_blank" style="text-decoration: none;">
            <div style="width:100%; background-color:#25D366; color:white; padding:18px; text-align:center; border-radius:12px; font-weight:bold; font-size:20px;">
                🟢 COMPARTIR POR WHATSAPP
            </div>
        </a>
    ''', unsafe_allow_html=True)

st.divider()
st.caption("AL REALIZAR UN GIRO SE DA POR LEÍDO LOS T&C")
