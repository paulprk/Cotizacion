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
    div.stButton > button:first-child {
        background-color: #1e3799;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
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
    /* Estilo para quitar bordes extras y centrar */
    input { text-align: center; }
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

# 4. Entradas de datos (Manual sin botones +/-)
col1, col2 = st.columns(2)
with col1:
    # Usamos text_input para evitar los botones de + y -
    monto_texto = st.text_input("Monto en USD:", value="100.00")
    try:
        dol = float(monto_texto.replace(",", "."))
    except ValueError:
        dol = 0.0
        st.error("Por favor, ingrese un número válido.")

with col2:
    comision_sel = st.radio("¿Comisión?", ["Incluida", "Aparte"])

st.write("") 
btn_cotizar = st.button("🚀 CALCULAR COTIZACIÓN")

# 5. Lógica de cálculo
if btn_cotizar:
    if dol > 0:
        MENOS_60 = 1.5
        MAS_60 = 0.025

        if dol <= 60:
            com_final = MENOS_60
        else:
            com_final = int(dol * MAS_60 * 100) / 100

        if comision_sel == "Incluida":
            monto_recibir_ars = round((dol - com_final) * COTIZACION_OFICIAL)
            monto_transferir_usd = dol
            txt_com = f"{com_final:.2f} USD (Incluida)"
        else:
            monto_recibir_ars = round(dol * COTIZACION_OFICIAL)
            monto_transferir_usd = dol + com_final
            txt_com = f"{com_final:.2f} USD (Aparte)"

        def fmt_ars(n):
            return f"{int(n):,}".replace(",", ".")
            
        def fmt_usd(n):
            return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        # 6. Recibo Visual
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 5px solid #2ecc71; color: black;">
            <p style="margin:5px 0;"><b>Monto:</b> {fmt_usd(dol)} USD</p>
            <p style="margin:5px 0;"><b>Comisión:</b> {txt_com}</p>
            <hr>
            <h2 style="color: #27ae60; margin:10px 0;">RECIBIR: {fmt_ars(monto_recibir_ars)} ARS</h2>
            <h2 style="color: #e67e22; margin:0;">TRANSFERIR: {fmt_usd(monto_transferir_usd)} USD</h2>
        </div>
        """, unsafe_allow_html=True)

        # 7. Mensaje de WhatsApp
        mensaje = (
            f"Hola buen día, esta es mi cotización:\n\n"
            f"*ARQUI GIROS*\n"
            f"------------------------------\n"
            f"📅 *Fecha:* {ahora}\n"
            f"💵 *Monto:* {fmt_usd(dol)} USD\n"
            f"⚙️ *Comisión:* {txt_com}\n\n"
            f"💰 *RECIBIR: {fmt_ars(monto_recibir_ars)} ARS*\n"
            f"💳 *TRANSFERIR: {fmt_usd(monto_transferir_usd)} USD*\n"
            f"------------------------------\n"
            f"Tasa aplicada: 1 USD = {int(COTIZACION_OFICIAL):,}\n\n".replace(",", ".") +
            f"Me ayudas con la cuenta por favor."
        )
        
        msg_encoded = urllib.parse.quote(mensaje)
        share_url = f"https://api.whatsapp.com/send?text={msg_encoded}"

        st.write("")
        st.markdown(f'''
            <a href="{share_url}" target="_blank" class="whatsapp-button">
                🟢 ENVIAR POR WHATSAPP
            </a>
            ''', unsafe_allow_html=True)
    else:
        st.warning("Por favor, ingrese un monto válido mayor a 0.")

st.divider()
st.caption("AL REALIZAR UN GIRO SE DA POR LEÍDO LOS T&C")
