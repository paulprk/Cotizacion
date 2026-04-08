import streamlit as st
from datetime import datetime, timedelta
import urllib.parse

# ==========================================
# CONFIGURACIÓN DE TASA (MODIFICA AQUÍ)
# ==========================================
COTIZACION_OFICIAL = 1445 # <-- Cambia este número cuando suba o baje el dólar
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
        height: 3.5em;
        width: 100%;
        font-weight: bold;
    }

    .whatsapp-btn {
        background-color: #25D366;
        color: white !important;
        padding: 15px;
        text-align: center;
        border-radius: 12px;
        font-weight: bold;
        font-size: 18px;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        margin-top: 10px;
    }
    .whatsapp-btn img { width: 25px; height: 25px; }
    
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

# 4. Entradas de datos
if 'calc_done' not in st.session_state:
    st.session_state.calc_done = False

# --- SECCIÓN DE MONTO Y COMISIÓN ---
col1, col2 = st.columns(2)
with col1:
    monto_texto = st.text_input("Monto en USD:", value="100.00", disabled=st.session_state.calc_done)
    try:
        dol = float(monto_texto.replace(",", "."))
    except ValueError:
        dol = 0.0
with col2:
    comision_sel = st.radio("¿Comisión?", ["Incluida", "Aparte"], disabled=st.session_state.calc_done)

# --- SECCIÓN DE BANCO REMITENTE ---
bancos_lista = ["Banco Pichincha", "Banco Guayaquil", "Banco Pacífico", "Banco Bolivariano", "Banco Internacional", "Otro"]
banco_sel = st.selectbox("Seleccione su banco remitente:", bancos_lista, disabled=st.session_state.calc_done)

banco_final = banco_sel
if banco_sel == "Otro":
    otro_banco = st.text_input("Nombre del banco:", placeholder="Ej: Produbanco", disabled=st.session_state.calc_done)
    banco_final = f"Banco {otro_banco}" if otro_banco else "Otro Banco"

# --- SECCIÓN DE DATOS DE DESTINO ---
col_cta1, col_cta2 = st.columns(2)
with col_cta1:
    cvu_cbu = st.text_input("CBU/CVU o Alias:", placeholder="Ingrese datos aquí", disabled=st.session_state.calc_done)
with col_cta2:
    nombre_titular = st.text_input("Nombre y Apellido:", placeholder="Titular de la cuenta", disabled=st.session_state.calc_done)

st.write("") 

# Botones de acción
if not st.session_state.calc_done:
    if st.button("🚀 CALCULAR COTIZACIÓN"):
        if dol > 0 and cvu_cbu and nombre_titular:
            st.session_state.calc_done = True
            st.rerun()
        else:
            st.error("Por favor, complete todos los campos (Monto, CBU/Alias y Nombre).")
else:
    # 5. Lógica de cálculo
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

    def fmt_ars(n): return f"{int(n):,}".replace(",", ".")
    def fmt_usd(n): return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # 6. Recibo Visual
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 5px solid #2ecc71; color: black; margin-bottom: 20px;">
        <p style="margin:5px 0;"><b>🏦 Banco Remitente:</b> {banco_final}</p>
        <p style="margin:5px 0;"><b>👤 Destinatario:</b> {nombre_titular.upper()}</p>
        <p style="margin:5px 0;"><b>🔑 CBU/CVU/Alias:</b> {cvu_cbu}</p>
        <hr>
        <p style="margin:5px 0;">Monto: {fmt_usd(dol)} USD | Comisión: {txt_com}</p>
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
        f"🏦 *Banco:* {banco_final}\n\n"
        f"💵 *Monto:* {fmt_usd(dol)} USD\n"
        f"⚙️ *Comisión:* {txt_com}\n"
        f"💰 *RECIBIR: {fmt_ars(monto_recibir_ars)} ARS*\n"
        f"💳 *TRANSFERIR: {fmt_usd(monto_transferir_usd)} USD*\n\n"
        f"------------------------------\n"
        f"*DATOS DE DESTINO:*\n"
        f"👤 *Nombre:* {nombre_titular.upper()}\n"
        f"🔑 *CBU/CVU/Alias:* {cvu_cbu}\n"
        f"------------------------------\n"
        f"Tasa aplicada: 1 USD = {int(COTIZACION_OFICIAL):,}\n\n".replace(",", ".") +
        f"Me ayudas con la cuenta por favor."
    )
    
    msg_encoded = urllib.parse.quote(mensaje)
    share_url = f"https://api.whatsapp.com/send?text={msg_encoded}"

    st.markdown(f'''
        <a href="{share_url}" target="_blank" class="whatsapp-btn">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg">
            ENVIAR POR WHATSAPP
        </a>
        ''', unsafe_allow_html=True)
    
    st.write("")
    if st.button("🔄 REALIZAR NUEVA COTIZACIÓN"):
        st.session_state.calc_done = False
        st.rerun()

st.divider()
st.caption("AL REALIZAR UN GIRO SE DA POR LEÍDO LOS T&C")
