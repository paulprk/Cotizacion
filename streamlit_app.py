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

# --- FUNCIÓN PARA CARGAR IMAGEN COMO BASE64 ---
# Esto es necesario para incrustar la imagen dentro del HTML del título
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# Intentamos cargar la imagen con tu nombre largo o el corto
# CAMBIA ESTO si renombras tu imagen en GitHub
img_name = "Gemini_Generated_Image_pz70wopz70wopz70.png"
# img_name = "logo.png" # Si la renombras, usa esta línea y comenta la de arriba

img_base64 = get_base64_image(img_name)

# Estilos CSS
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stRadio > div { flex-direction: row; justify-content: center; }
    
    /* Estilo del Título Integrado (Logo + Texto) */
    .arqui-title {
        text-align: center;
        color: #1e3799;
        font-weight: bold;
        font-size: 36px; /* Tamaño del título principal */
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px; /* Espacio entre logo y texto */
        margin-bottom: 5px;
    }

    /* Estilo para el Logo dentro del Título (Mismo tamaño que texto) */
    .title-logo {
        height: 36px; /* Mismo height que el font-size del título */
        width: auto;
    }

    /* Estilo para el Texto de Cotización Centrado */
    .cotizacion-box {
        text-align: center;
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        color: #31333F;
        margin-top: -5px;
        margin-bottom: 20px;
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

    /* Botón WhatsApp - Rectangular y Compacto (Anti-errores Android) */
    .whatsapp-btn-active {
        background-color: #25D366;
        color: white !important;
        padding: 8px 16px;
        text-align: center;
        border-radius: 8px; /* Rectangular suavizado */
        font-weight: 600;
        font-size: 14px;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.1);
        border: none;
    }

    .whatsapp-btn-inactive {
        background-color: #e0e0e0;
        color: #888888 !important;
        padding: 8px 16px;
        text-align: center;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        pointer-events: none;
    }
    
    .whatsapp-btn img { width: 18px; height: 18px; }
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

# --- ENCABEZADO INTEGRADO (Logo + Texto) ---
# Creamos el HTML dinámico para el título
title_html = '<div class="arqui-title">'
if img_base64:
    # Si la imagen existe, la insertamos como Base64
    title_html += f'<img src="data:image/png;base64,{img_base64}" class="title-logo">'
else:
    # Si no, mostramos el emoji original como respaldo
    title_html += '🏦 '
title_html += 'Arqui Giros</div>'

# Mostramos el título integrado
st.markdown(title_html, unsafe_allow_html=True)

# Texto de cotización centrado justo debajo
st.markdown(f'<div class="cotizacion-box">Cotización: 1 USD = {COTIZACION_OFICIAL:,} ARS</div>'.replace(",", "."), unsafe_allow_html=True)

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

    # Botón centrado y ajustado
    st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
    if datos_completos:
        st.markdown(f'''
            <a href="{share_url}" target="_blank" class="whatsapp-btn-active">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg">
                Enviar WhatsApp
            </a>
            ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
            <div class="whatsapp-btn-inactive">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" style="filter: grayscale(1);">
                Completar datos
            </div>
            ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    if st.button("🔄 REALIZAR NUEVA COTIZACIÓN"):
        st.session_state.calc_step = False
        st.rerun()

st.divider()
st.caption("AL REALIZAR UN GIRO SE DA POR LEÍDO LOS T&C")
