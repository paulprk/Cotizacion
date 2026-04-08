import streamlit as st
from datetime import datetime, timedelta
import urllib.parse

# ==========================================
# CONFIGURACIÓN DE TASA (MODIFICA AQUÍ)
# ==========================================
COTIZACION_OFICIAL = 1445
# ==========================================

st.set_page_config(page_title="Arqui Giros - Oficial", page_icon="💸")

# Estilos CSS
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stRadio > div { flex-direction: row; justify-content: center; }
    
    /* Centrado del encabezado (Logo y Cotización) */
    .header-container {
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin-bottom: 20px;
    }

    .cotizacion-text {
        font-size: 20px;
        font-weight: bold;
        color: #31333F;
        margin-top: 10px;
        text-align: center;
    }

    /* Botón Calcular Principal */
    div.stButton > button:first-child {
        background-color: #1e3799;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }

    /* Botón WhatsApp - Alargado y Fino (según dibujo de image_22.png) */
    .whatsapp-btn-active {
        background-color: #25D366;
        color: white !important;
        padding: 8px 15px; /* Menos padding vertical para hacerlo fino */
        text-align: center;
        border-radius: 8px;
        font-weight: 600;
        font-size: 16px;
        text-decoration: none;
        display: flex; /* Alargado horizontal */
        align-items: center;
        justify-content: center;
        gap: 8px;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.1);
        width: 100%; /* Ocupa el ancho */
        margin-top: 10px;
    }

    .whatsapp-btn-inactive {
        background-color: #e0e0e0;
        color: #888888 !important;
        padding: 8px 15px;
        text-align: center;
        border-radius: 8px;
        font-weight: 600;
        font-size: 16px;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        width: 100%;
        margin-top: 10px;
        pointer-events: none;
    }
    
    /* Icono de WhatsApp Micro */
    .whatsapp-btn img { 
        width: 18px !important; 
        height: 18px !important; 
    }
    
    input { text-align: center; }
    
    .comision-info {
        text-align: center;
        font-size: 13px;
        color: #666;
        margin-top: -10px;
        margin-bottom: 10px;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

ahora_arg = datetime.utcnow() - timedelta(hours=3)
ahora = ahora_arg.strftime("%d/%m/%Y %H:%M")

# 3. Encabezado Centrado (Logo y Cotización)
st.markdown('<div class="header-container">', unsafe_allow_html=True)
try:
    # Intenta cargar con el nombre largo, si falla intenta con logo.png
    st.image("Gemini_Generated_Image_pz70wopz70wopz70.png", width=220)
except:
    try:
        st.image("logo.png", width=220)
    except:
        # Texto de respaldo si no hay imagen
        st.markdown("<h1 style='text-align: center; color: #1e3799;'>🏦 ARQUI GIROS</h1>", unsafe_allow_html=True)

st.markdown(f'<p class="cotizacion-text">Cotización: 1 USD = {COTIZACION_OFICIAL:,} ARS</p>'.replace(",", "."), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.divider()

if 'calc_step' not in st.session_state:
    st.session_state.calc_step = False

# PASO 1: ENTRADA BÁSICA
col1, col2 = st.columns(2)
with col1:
    monto_texto = st.text_input("Monto en USD:", value="100.00", disabled=st.session_state.calc_step)
    try:
        dol = float(monto_texto.replace(",", "."))
    except ValueError:
        dol = 0.0
with col2:
    comision_sel = st.radio("Comisión", ["Incluida", "Aparte"], disabled=st.session_state.calc_step)
    if comision_sel == "Incluida":
        st.markdown('<p class="comision-info">Se descuenta del monto enviado</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="comision-info">Se suma al valor a enviar</p>', unsafe_allow_html=True)

if not st.session_state.calc_step:
    if st.button("🚀 CALCULAR COTIZACIÓN"):
        if dol > 0:
            st.session_state.calc_step = True
            st.rerun()
        else:
            st.error("Ingrese un monto válido.")

# PASO 2: MOSTRAR RESULTADO Y PEDIR DATOS EXTRAS
if st.session_state.calc_step:
    MENOS_60 = 1.5
    MAS_60 = 0.025
    com_final = MENOS_60 if dol <= 60 else int(dol * MAS_60 * 100) / 100

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

    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 5px solid #2ecc71; color: black; margin-bottom: 20px;">
        <h2 style="color: #27ae60; margin:0; text-align: center;">RECIBIR: {fmt_ars(monto_recibir_ars)} ARS</h2>
        <p style="margin:5px 0; text-align: center;">Monto: {fmt_usd(dol)} USD | Comisión: {txt_com}</p>
        <p style="color: #e67e22; margin:0; font-weight:bold; text-align: center;">Transferir: {fmt_usd(monto_transferir_usd)} USD</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📝 Datos para el Recibo")
    bancos_lista = ["Banco Pichincha", "Banco Guayaquil", "Banco Pacífico", "Banco Bolivariano", "Banco Internacional", "Otro"]
    banco_sel = st.selectbox("Seleccione su banco remitente:", bancos_lista)
    
    banco_final = banco_sel
    if banco_sel == "Otro":
        otro_banco = st.text_input("Especifique su banco:", placeholder="Ej. Produbanco")
        banco_final = f"Banco {otro_banco}" if otro_banco else "Otro Banco"

    c_cta1, c_cta2 = st.columns(2)
    with c_cta1:
        cvu_cbu = st.text_input("Ingrese su CVU/CBU o Alias:", placeholder="Ingrese Información")
    with c_cta2:
        nombre_titular = st.text_input("Ingrese nombre y apellido:", placeholder="Ingrese su Nombre y Apellido")

    datos_completos = cvu_cbu.strip() != "" and nombre_titular.strip() != ""
    
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

    # Botón de WhatsApp estilizado (Alargado y Fino)
    if datos_completos:
        st.markdown(f'''
            <a href="{share_url}" target="_blank" class="whatsapp-btn-active">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg">
                ENVIAR POR WHATSAPP
            </a>
            ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
            <div class="whatsapp-btn-inactive">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" style="filter: grayscale(1);">
                COMPLETE DATOS PARA ENVIAR
            </div>
            ''', unsafe_allow_html=True)
        st.caption("<p style='text-align: center;'>⚠️ Por favor complete el CBU y Nombre.</p>", unsafe_allow_html=True)

    st.write("")
    if st.button("🔄 REALIZAR NUEVA COTIZACIÓN"):
        st.session_state.calc_step = False
        st.rerun()

st.divider()
st.caption("AL REALIZAR UN GIRO SE DA POR LEÍDO LOS T&C")
