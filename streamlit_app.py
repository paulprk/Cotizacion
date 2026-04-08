import streamlit as st
from datetime import datetime, timedelta
import urllib.parse

# ==========================================
# CONFIGURACIÓN DE TASA (MODIFICA AQUÍ)
# ==========================================
COTIZACION_OFICIAL = 1445  
# ==========================================

st.set_page_config(page_title="Arqui Giros - Oficial", page_icon="💸")

# Estilos CSS dinámicos
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stRadio > div { flex-direction: row; justify-content: center; }
    
    /* Botón Calcular Principal */
    div.stButton > button:first-child {
        background-color: #1e3799;
        color: white;
        border-radius: 10px;
        height: 3.5em;
        width: 100%;
        font-weight: bold;
    }

    /* Botón WhatsApp Verde */
    .whatsapp-btn-active {
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
    }

    /* Botón WhatsApp Gris (Inactivo) */
    .whatsapp-btn-inactive {
        background-color: #d1d1d1;
        color: #7a7a7a !important;
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
        pointer-events: none;
    }
    .whatsapp-btn img { width: 25px; height: 25px; }
    input { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

ahora_arg = datetime.utcnow() - timedelta(hours=3)
ahora = ahora_arg.strftime("%d/%m/%Y %H:%M")

# Encabezado
col_logo1, col_logo2, col_logo3 = st.columns([1,2,1])
with col_logo2:
    try:
        st.image("logo.png", width=200)
    except:
        st.markdown("<h1 style='text-align: center; color: #1e3799;'>🏦 ARQUI GIROS</h1>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center; font-size: 20px;'><b>Cotización:</b> 1 USD = {COTIZACION_OFICIAL:,} ARS</p>".replace(",", "."), unsafe_allow_html=True)
st.divider()

# Iniciar estado si no existe
if 'calc_step' not in st.session_state:
    st.session_state.calc_step = False

# PASO 1: ENTRADA BÁSICA (Monto y Comisión)
col1, col2 = st.columns(2)
with col1:
    monto_texto = st.text_input("Monto en USD:", value="100.00", disabled=st.session_state.calc_step)
    try:
        dol = float(monto_texto.replace(",", "."))
    except ValueError:
        dol = 0.0
with col2:
    comision_sel = st.radio("¿Comisión?", ["Incluida", "Aparte"], disabled=st.session_state.calc_step)

if not st.session_state.calc_step:
    if st.button("🚀 CALCULAR COTIZACIÓN"):
        if dol > 0:
            st.session_state.calc_step = True
            st.rerun()
        else:
            st.error("Ingrese un monto válido.")

# PASO 2: MOSTRAR RESULTADO Y PEDIR DATOS EXTRAS
if st.session_state.calc_step:
    # Lógica de cálculo
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

    # Recibo Visual (Resultado de cotización)
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 5px solid #2ecc71; color: black; margin-bottom: 20px;">
        <h2 style="color: #27ae60; margin:0;">RECIBIR: {fmt_ars(monto_recibir_ars)} ARS</h2>
        <p style="margin:5px 0;">Monto: {fmt_usd(dol)} USD | Comisión: {txt_com}</p>
        <p style="color: #e67e22; margin:0; font-weight:bold;">Transferir: {fmt_usd(monto_transferir_usd)} USD</p>
    </div>
    """, unsafe_allow_html=True)

    # DATOS DE DESTINO (Aparecen después de cotizar)
    st.markdown("### 📝 Datos para el Recibo (Opcional)")
    bancos_lista = ["Banco Pichincha", "Banco Guayaquil", "Banco Pacífico", "Banco Bolivariano", "Banco Internacional", "Otro"]
    banco_sel = st.selectbox("Banco remitente:", bancos_lista)
    
    banco_final = banco_sel
    if banco_sel == "Otro":
        otro_banco = st.text_input("Especifique banco:")
        banco_final = f"Banco {otro_banco}" if otro_banco else "Otro Banco"

    c_cta1, c_cta2 = st.columns(2)
    with c_cta1:
        cvu_cbu = st.text_input("CBU/CVU o Alias:")
    with c_cta2:
        nombre_titular = st.text_input("Nombre y Apellido:")

    # VALIDACIÓN PARA EL BOTÓN DE WHATSAPP
    datos_completos = cvu_cbu.strip() != "" and nombre_titular.strip() != ""
    
    # Preparar mensaje
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

    # Botón dinámico de WhatsApp
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
        st.caption("⚠️ Ingrese CBU y Nombre para habilitar el envío.")

    st.write("")
    if st.button("🔄 NUEVA COTIZACIÓN"):
        st.session_state.calc_step = False
        st.rerun()

st.divider()
st.caption("AL REALIZAR UN GIRO SE DA POR LEÍDO LOS T&C")
