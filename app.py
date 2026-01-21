# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 21:33:27 2026

@author: TrendingPc
"""

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import random
import re

# --- CONFIGURACIÓN DE LOS 3 PLANES ---
PLANES = {
    "Puntual": {"limite": 1, "precio": "1€"},
    "Profesional": {"limite": 5, "precio": "5€"},
    "Ilimitado": {"limite": 9999, "precio": "10€"}
}

# --- 1. GESTIÓN DE USUARIOS (SIMULADA PARA MVP) ---
# En una fase avanzada usaríamos una base de datos real. 
# De momento, el usuario se "loguea" para activar su plan.

st.set_page_config(page_title="GML Pro - Gestión de Planes", layout="wide")

if 'descargas_realizadas' not in st.session_state:
    st.session_state.descargas_realizadas = 0

# --- INTERFAZ DE USUARIO ---
st.title("📐 Generador GML con Suscripción")

# Login lateral
with st.sidebar:
    st.header("👤 Mi Cuenta")
    opcion = st.radio("Acceso", ["Iniciar Sesión / Registro", "Mi Suscripción"])
    
    if opcion == "Iniciar Sesión / Registro":
        st.text_input("Email o Gmail")
        st.text_input("Contraseña", type="password")
        st.button("Entrar")
        st.button("Registrarse con Google") # Aquí conectarías Firebase o Auth0 más adelante
    else:
        st.write("**Plan Actual:** Ninguno")
        st.info("Suscríbete para descargar")

# --- SELECTOR DE PLANES (VISUAL) ---
st.subheader("Selecciona tu plan de descargas")
cols = st.columns(3)
for i, (nombre, info) in enumerate(PLANES.items()):
    with cols[i]:
        st.markdown(f"### {nombre}")
        st.write(f"**{info['precio']} / mes**")
        st.write(f"Límite: {info['limite']} GMLs")
        if st.button(f"Elegir {nombre}", key=nombre):
            st.write(f"Redirigiendo a Stripe para {nombre}...")

st.divider()

# --- LA HERRAMIENTA (EL CÓDIGO) ---
rc_base = st.text_input("Referencia Catastral")
datos_autocad = st.text_area("Pega aquí el comando LIST")

if st.button("Procesar y Generar GML"):
    # Lógica de cálculo (la que ya tenemos)
    puntos = re.findall(r"X=\s*([\d\.-]+)\s+Y=\s*([\d\.-]+)", datos_autocad)
    
    if puntos and rc_base:
        # ID aleatorio según tu regla [2026-01-15]
        rc_id = f"{rc_base}_{random.randint(0, 999):03d}"
        
        st.success(f"Archivo listo: {rc_id}")
        
        # LÓGICA DE CONTROL DE DESCARGAS
        plan_usuario = "Profesional" # Ejemplo: simulamos que el usuario tiene este plan
        limite = PLANES[plan_usuario]["limite"]
        
        if st.session_state.descargas_realizadas < limite:
            if st.download_button("📥 DESCARGAR AHORA", data="CONTENIDO_GML", file_name=f"{rc_id}.gml"):
                st.session_state.descargas_realizadas += 1
            st.write(f"Has usado {st.session_state.descargas_realizadas} de {limite} descargas mensuales.")
        else:
            st.error("❌ Has agotado tu límite mensual. Sube de plan para seguir.")
