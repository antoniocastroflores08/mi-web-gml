# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 21:33:27 2026

@author: TrendingPc
"""

import streamlit as st
import re
import random
import datetime

# 1. IDENTIDAD DE TU MARCA
st.set_page_config(page_title="GML Express - Generador Catastral", page_icon="📐")

st.title("📐 GML Express")
st.subheader("Genera tus archivos GML válidos en segundos")

# 2. SECCIÓN DE PAGO (Aquí pegarás lo de Stripe más adelante)
with st.sidebar:
    st.header("Suscripción")
    st.write("Plan actual: **Gratuito (Solo lectura)**")
    st.info("Suscríbete por 1€/mes para descargar tus archivos.")
    # Aquí es donde pondremos el enlace a tu tabla de Stripe
    st.markdown("[👉 Ver Planes de Suscripción](https://tu-enlace-de-stripe.com)")

# 3. LA HERRAMIENTA
rc_base = st.text_input("Introduce la Referencia Catastral (20 caracteres)")
tipo_gml = st.radio("¿Qué quieres generar?", ["Parcela (GML WFS)", "Edificio (GML Building)"])
datos_autocad = st.text_area("Pega aquí el resultado del comando LIST de AutoCAD", height=250)

if st.button("Generar y Validar Geometría"):
    if len(rc_base) < 14:
        st.error("Por favor, introduce una Referencia Catastral válida.")
    elif not datos_autocad:
        st.warning("Pega los puntos de AutoCAD para continuar.")
    else:
        # Extraer coordenadas
        matches = re.findall(r"X=\s*([\d\.-]+)\s+Y=\s*([\d\.-]+)", datos_autocad)
        
        if matches:
            # Tu regla personalizada de ID: RC + _ + 3 dígitos aleatorios
            sufijo = f"{random.randint(0, 999):03d}"
            rc_id = f"{rc_base}_{sufijo}"
            
            # Cálculo de área (Gauss)
            puntos = [(float(x), float(y)) for x, y in matches]
            if puntos[0] != puntos[-1]: puntos.append(puntos[0])
            area = 0.0
            for i in range(len(puntos)):
                j = (i + 1) % len(puntos)
                area += puntos[i][0] * puntos[j][1]
                area -= puntos[j][0] * puntos[i][1]
            area_final = abs(area) / 2.0
            
            st.success(f"✅ Geometría procesada correctamente. Área: {area_final:.2f} m2")
            st.code(f"ID del archivo: {rc_id}", language="text")
            
            # BLOQUEO DE DESCARGA PARA SUSCRIPTORES
            st.warning("🔒 La descarga de archivos GML está reservada para usuarios con suscripción.")
            st.button("Descargar GML (Bloqueado)", disabled=True)
        else:
            st.error("No se han encontrado coordenadas válidas. Asegúrate de copiar el texto completo de AutoCAD.")

st.markdown("---")
st.caption("© 2026 GML Express - Herramienta para técnicos y topógrafos.")