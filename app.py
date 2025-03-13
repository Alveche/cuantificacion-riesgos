import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Ponderación de sectores para cada riesgo
SECTOR_PONDERACION = {
    "Riesgo de Endeudamiento": {
        "Infraestructura": 3, "Bienes Raíces": 3, "Energía": 3,
        "Retail": 2, "Industria": 2, "Salud": 2, "Finanzas": 2,
        "Tecnología": 1, "Consultoría": 1
    },
    "Riesgo de Ciberataque": {
        "Finanzas": 3, "Salud": 3,
        "Retail": 2, "Energía": 2, "Industria": 2,
        "Bienes Raíces": 1, "Infraestructura": 1, "Tecnología": 1, "Consultoría": 1
    }
}

def obtener_cuestionario(riesgo):
    respuestas = {}

    if riesgo == "Riesgo de Liquidez":
        respuestas["liquidez_disponible"] = st.number_input("¿Cuál es el nivel actual de liquidez disponible? (€)", min_value=0.0, step=1000.0)
        respuestas["flujo_caja"] = st.number_input("¿Cuál es el flujo de caja promedio mensual? (€)", min_value=0.0, step=1000.0)
        respuestas["deuda_corto_plazo"] = st.number_input("¿Cuál es la deuda a corto plazo en comparación con los activos líquidos? (%)", min_value=0.0, step=1.0)
        respuestas["lineas_credito"] = st.selectbox("¿Existen líneas de crédito disponibles?", ["Sí", "No"])
        respuestas["ingresos_diferidos"] = st.number_input("¿Qué porcentaje de ingresos proviene de clientes con pagos diferidos? (%)", min_value=0.0, step=1.0)
    
    elif riesgo == "Riesgo de Crédito":
        respuestas["morosidad"] = st.number_input("¿Cuál es el porcentaje de clientes con pagos atrasados? (%)", min_value=0.0, step=1.0)
        respuestas["rating_crediticio"] = st.selectbox("¿Cuál es el rating crediticio promedio de los clientes?", ["AAA", "AA", "A", "BBB", "BB", "B", "C"])
        respuestas["diversificacion_clientes"] = st.number_input("¿Cuántos clientes representan más del 50% de los ingresos?", min_value=0, step=1)
        respuestas["politicas_credito"] = st.selectbox("¿La empresa cuenta con políticas de crédito estrictas?", ["Sí", "No"])
    
    return respuestas

def procesar_respuestas(datos_generales, respuestas_riesgo, riesgo):
    peso_factor = 0.2
    valores_numericos = [v for v in respuestas_riesgo.values() if isinstance(v, (int, float))]
    
    # Ponderación del sector en el índice de riesgo
    sector = datos_generales.get("sector")
    sector_ponderacion = SECTOR_PONDERACION.get(riesgo, {}).get(sector, 1)
    
    if valores_numericos:
        indice_riesgo = (sum(valores_numericos) / len(valores_numericos)) * peso_factor * sector_ponderacion
    else:
        indice_riesgo = None
    
    return {"riesgo": riesgo, "indice": round(indice_riesgo, 2) if indice_riesgo is not None else "Datos insuficientes"}

def main():
    st.title("Herramienta de Cuantificación de Riesgos")
    
    st.subheader("Paso 1: Datos Generales de la Compañía")
    datos_generales = {
        "facturacion": st.number_input("Facturación anual (€)", min_value=0.0, step=10000.0),
        "sociedades": st.number_input("Número de sociedades que participan", min_value=1, step=1),
        "empleados": st.number_input("Número de empleados", min_value=1, step=1),
        "sector": st.selectbox("Sector en el que opera", ["Finanzas", "Energía", "Retail", "Tecnología", "Salud", "Industria", "Infraestructura", "Bienes Raíces", "Consultoría"]),
        "paises": st.number_input("Número de países en los que opera", min_value=1, step=1),
        "modelo_negocio": st.selectbox("Modelo de negocio", ["B2B", "B2C", "Mixto"]),
        "infraestructura": st.selectbox("Infraestructura tecnológica", ["Baja", "Media", "Alta"]),
        "comercio_digital": st.selectbox("Comercio digital", ["Sí", "No"])
    }
    
    st.subheader("Paso 2: Selección del Riesgo a Cuantificar")
    riesgo = st.selectbox("¿Qué riesgo quieres cuantificar?", ["Riesgo de Liquidez", "Riesgo de Crédito", "Riesgo de Mercado", "Riesgo de Endeudamiento", "Riesgo de Ciberataque"])
    
    st.subheader("Paso 3: Cuestionario Específico del Riesgo")
    respuestas_riesgo = obtener_cuestionario(riesgo)
    
    if st.button("Procesar Información"):
        st.subheader("Paso 4: Procesamiento de Respuestas")
        datos_procesados = procesar_respuestas(datos_generales, respuestas_riesgo, riesgo)
        
        if isinstance(datos_procesados["indice"], str):
            st.warning(datos_procesados["indice"])
        else:
            st.write("Datos procesados:", datos_procesados)

if __name__ == "__main__":
    main()
