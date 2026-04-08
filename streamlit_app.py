import streamlit as st
from datetime import datetime, timedelta
import urllib.parse
import base64
import os

# ==========================================
# CONFIGURACIÓN DE TASAS (MODIFICA AQUÍ)
# ==========================================
TASA_USD_A_ARS = 1445  # Lo que recibe el cliente en ARS
TASA_ARS_A_USD = 1505  # Lo que debe entregar el cliente en ARS
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

    /* Caja de Cotizaciones Dual */
    .cotizacion-container {
        text-align: center;
        width: 100%;
        margin-bottom: 20px;
    }

    .cotizacion-box {
        font-size: 18px;
        font-weight: bold;
        color: #31333F;
        margin: 2px 0;
    }

    div.stButton > button:first-child {
        background-color: #1e3799; color: white; border-radius: 8px;
        height: 3em; width: 100%; font-weight: bold;
    }

    .stButton > button[kind="secondary"] {
        width: fit-content !important; padding: 4px 15px !important;
        font-size: 13px !important; margin: 0 auto; display: block;
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

# Mostrar Doble Cotización
st.markdown(f"""
    <div class="cotizacion-container">
        <div class="cotizacion-box">Cotización: </div>
        <div class="cotizacion-box">1 USD = {TASA_USD_A_ARS:,} ARS</div>
        <div class="cotizacion-box">{TASA_ARS_A_USD:,} ARS = 1 USD</div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

st.divider()

# --- SELECTOR DE APARTADO ---
opcion = st.selectbox("Seleccione el tipo de operación:", 
                      ["Seleccione una opción...", "💵 Dólares a Pesos", "🇦🇷 Pesos a Dólares"])

if opcion == "💵 Dólares a Pesos":
    if 'calc_step' not in st.session_state:
        st.session_state.calc_step = False

    col1, col2 = st.columns(2)
    with col1:
        monto_texto = st.text_input("Monto en USD:", value="100.00", disabled=st.session_state.calc_step)
        try: dol = float(monto_texto.replace(",", "."))
        except ValueError: dol = 0.0
    with col2:
        comision_sel = st.radio("Comisión", ["Incluida", "Aparte"], disabled=st.session_state.calc_step)
        
        # --- MODIFICA ESTA LÍNEA ---
        if comision_sel == "Incluida":
            text_com = "La comisión se descuenta del valor<br><span style='font-size: 10px;'>(monto - comisión)</span>"
        else:
            text_com = "La comisión se suma al valor a enviar<br><span style='font-size: 10px;'>(monto + comisión)</span>"
        
        st.markdown(f'<p class="comision-info">{text_com}</p>', unsafe_allow_html=True)

    if not st.session_state.calc_step:
        if st.button("🚀 CALCULAR COTIZACIÓN"):
            if dol > 0:
                st.session_state.calc_step = True
                st.rerun()

    if st.session_state.calc_step:
        com_final = 1.5 if dol <= 60 else int(dol * 0.025 * 100) / 100
        if comision_sel == "Incluida":
            recibir = round((dol - com_final) * TASA_USD_A_ARS)
            transferir = dol
        else:
            recibir = round(dol * TASA_USD_A_ARS)
            transferir = dol + com_final

        def f_ars(n): return f"{int(n):,}".replace(",", ".")
        def f_usd(n): return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 12px; border-left: 5px solid #2ecc71; color: black; margin-bottom: 20px; text-align:center;">
            <h2 style="color: #27ae60; margin:0;">RECIBIR: {f_ars(recibir)} ARS</h2>
            <p style="margin:5px 0; font-size:14px;">Monto: {f_usd(dol)} USD | Comisión: {com_final:.2f} USD</p>
            <p style="color: #e67e22; margin:0; font-weight:bold;">Transferir: {f_usd(transferir)} USD</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📝 Datos de Destino")
        banco_sel = st.selectbox("Banco remitente:", ["Banco Pichincha", "Banco Guayaquil", "Banco Pacífico", "Banco Bolivariano", "Banco Internacional", "Otro"])
        if banco_sel == "Otro":
            banco_final = f"Banco {st.text_input('Especifique banco:', placeholder='Ej. Produbanco')}"
        else: banco_final = banco_sel

        c1, c2 = st.columns(2)
        with c1: cvu = st.text_input("CBU/CVU o Alias:", placeholder="Ingrese información")
        with c2: nombre = st.text_input("Nombre y Apellido:", placeholder="Ingrese nombre")

        ws_icon_url = "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg"
        msg = urllib.parse.quote(f"Hola Arqui Giros, cotización USD a ARS:\n\n*Recibir:* {f_ars(recibir)} ARS\n*Banco:* {banco_final}\n*Destino:* {nombre.upper()}\n*CBU:* {cvu}\n\nAyúdame con la cuenta.")
        
        if cvu and nombre:
            st.markdown(f'<div class="whatsapp-link"><a href="https://api.whatsapp.com/send?text={msg}" target="_blank" class="btn-ws bg-active"><img src="{ws_icon_url}" class="ws-icon"> Compartir a WhatsApp</a></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'''
                <div class="whatsapp-link" style="flex-direction: column; align-items: center;">
                    <div class="btn-ws bg-inactive"><img src="{ws_icon_url}" class="ws-icon" style="filter:grayscale(1)"> Compartir a WhatsApp</div>
                    <p style="color: #ff4b4b; font-size: 13px; margin-top: 8px; font-weight: bold; text-align: center;">
                        ⚠️ Complete los datos para compartir a WhatsApp
                    </p>
                </div>''', unsafe_allow_html=True)

        st.write("")
        if st.button("🔄 NUEVA COTIZACIÓN"):
            st.session_state.calc_step = False
            st.rerun()

elif opcion == "🇦🇷 Pesos a Dólares":
    if 'calc_step_ars' not in st.session_state:
        st.session_state.calc_step_ars = False

    # Selector de tipo de cálculo
    tipo_calculo = st.radio("¿Qué desea calcular?", 
                             ["Saber cuántos USD recibo (tengo Pesos)", "Saber cuántos ARS necesito (necesito USD)"])

    # Entrada de monto
    if "recibo" in tipo_calculo:
        monto_ars_in = st.text_input("Cantidad en Pesos (ARS):", value="150.500", disabled=st.session_state.calc_step_ars)
        try: monto_usr = float(monto_ars_in.replace(".", "").replace(",", "."))
        except: monto_usr = 0.0
    else:
        monto_usd_in = st.text_input("Cantidad en Dólares (USD):", value="100.00", disabled=st.session_state.calc_step_ars)
        try: monto_usr = float(monto_usd_in.replace(",", "."))
        except: monto_usr = 0.0

    if not st.session_state.calc_step_ars:
        if st.button("🚀 CALCULAR COTIZACIÓN", key="btn_ars"):
            if monto_usr > 0:
                st.session_state.calc_step_ars = True
                st.rerun()

    if st.session_state.calc_step_ars:
        # CÁLCULOS
        if "recibo" in tipo_calculo:
            recibir_final = monto_usr / TASA_ARS_A_USD
            pagar_final = monto_usr
        else:
            recibir_final = monto_usr
            pagar_final = monto_usr * TASA_ARS_A_USD

        def f_ars(n): return f"{int(n):,}".replace(",", ".")
        def f_usd(n): return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        # RECUADRO DE RESULTADO (CORREGIDO SIN COMISION)
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 12px; border-left: 5px solid #3498db; color: black; margin-bottom: 20px; text-align:center;">
            <h2 style="color: #2980b9; margin:0;">RECIBIR: {f_usd(recibir_final)} USD</h2>
            <p style="margin:5px 0; font-size:14px;">Tasa aplicada: 1 USD = {TASA_ARS_A_USD:,} ARS</p>
            <p style="color: #e67e22; margin:0; font-weight:bold;">Entregar: {f_ars(pagar_final)} ARS</p>
        </div>
        """.replace(",", "."), unsafe_allow_html=True)

        st.markdown("### 📝 Datos de Destino (Exterior)")
        banco_ars = st.selectbox("Banco del exterior:", ["Banco Pichincha", "Banco Guayaquil", "Banco Pacífico", "Banco Bolivariano", "Otro"], key="b_ars")
        banco_f = st.text_input("Especifique banco:", placeholder="Ej. Banco del Austro") if banco_ars == "Otro" else banco_ars

        tipo_cta = st.selectbox("Tipo de cuenta:", ["Ahorros", "Corriente"])
        
        c1, c2 = st.columns(2)
        with c1: n_cta = st.text_input("Número de cuenta:", placeholder="Ej. 2200123456")
        with c2: cedula = st.text_input("Número de cédula:", placeholder="Ej. 1712345678")
        
        nom_ape = st.text_input("Nombre y Apellido del beneficiario:", placeholder="Nombre completo")

        # WHATSAPP (CORREGIDO SIN VARIABLES INEXISTENTES)
        ws_url = "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg"
        
        # Armamos el mensaje de texto puro primero para evitar errores de llaves
        texto_mensaje = (
            f"Hola Arqui Giros, cotización ARS a USD:\n\n"
            f"*Entregar:* {f_ars(pagar_final)} ARS\n"
            f"*Recibir:* {f_usd(recibir_final)} USD\n"
            f"--------------------------\n"
            f"*DATOS DESTINO:*\n"
            f"*Banco:* {banco_f}\n"
            f"*Cuenta:* {tipo_cta} - {n_cta}\n"
            f"*Cédula:* {cedula}\n"
            f"*Nombre:* {nom_ape.upper()}\n\n"
            f"Me confirmas para enviarte los pesos."
        )
        msg_ars = urllib.parse.quote(texto_mensaje)

        if n_cta and cedula and nom_ape:
            st.markdown(f'<div class="whatsapp-link"><a href="https://api.whatsapp.com/send?text={msg_ars}" target="_blank" class="btn-ws bg-active"><img src="{ws_url}" class="ws-icon"> Compartir a WhatsApp</a></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'''
                <div class="whatsapp-link" style="flex-direction: column; align-items: center;">
                    <div class="btn-ws bg-inactive"><img src="{ws_url}" class="ws-icon" style="filter:grayscale(1)"> Compartir a WhatsApp</div>
                    <p style="color: #ff4b4b; font-size: 13px; margin-top: 8px; font-weight: bold; text-align: center;">⚠️ Complete los datos para compartir</p>
                </div>''', unsafe_allow_html=True)

        st.write("")
        if st.button("🔄 NUEVA COTIZACIÓN", key="reset_ars"):
            st.session_state.calc_step_ars = False
            st.rerun()

else:
    st.write("👋 ¡Bienvenido! Por favor, selecciona arriba qué tipo de cambio deseas realizar para comenzar.")

st.divider()
st.caption("AL REALIZAR UN GIRO SE DA POR LEÍDO LOS T&C")
