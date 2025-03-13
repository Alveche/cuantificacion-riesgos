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
    
    elif riesgo == "Riesgo de Mercado":
        respuestas["volatilidad_activos"] = st.number_input("¿Cuál es la volatilidad de los activos de la empresa? (%)", min_value=0.0, step=0.1)
        respuestas["exposicion_divisas"] = st.selectbox("¿La empresa opera en múltiples divisas?", ["Sí", "No"])
        respuestas["sensibilidad_tasa_interes"] = st.number_input("¿Cuánto afectarían las tasas de interés a los costos financieros? (%)", min_value=0.0, step=0.1)
    
    elif riesgo == "Riesgo de Endeudamiento":
        respuestas["ratio_endeudamiento"] = st.number_input("¿Cuál es el ratio de endeudamiento actual? (%)", min_value=0.0, step=1.0)
        respuestas["capacidad_pago"] = st.selectbox("¿La empresa tiene capacidad de pago a corto plazo?", ["Sí", "No"])
        respuestas["cobertura_intereses"] = st.number_input("¿Cuál es la cobertura de intereses sobre deuda? (veces)", min_value=0.0, step=0.1)
    
    elif riesgo == "Riesgo de Ciberataque":
        respuestas["ataques_recientes"] = st.selectbox("¿La empresa ha sufrido ciberataques en los últimos 12 meses?", ["Sí", "No"])
        respuestas["proteccion_datos"] = st.selectbox("¿La empresa cuenta con cifrado de datos sensibles?", ["Sí", "No"])
        respuestas["plan_respuesta"] = st.selectbox("¿Existe un plan de respuesta ante incidentes?", ["Sí", "No"])
        respuestas["nivel_seguridad"] = st.selectbox("¿Cómo calificarías la seguridad informática de la empresa?", ["Baja", "Media", "Alta"])
    
    return respuestas

def convertir_categoricas(respuestas):
    conversion = {"Sí": 1, "No": 3, "AAA": 1, "AA": 2, "A": 3, "BBB": 4, "BB": 5, "B": 6, "C": 7, "Baja": 3, "Media": 2, "Alta": 1}
    return {k: conversion.get(v, v) for k, v in respuestas.items()}

def procesar_respuestas(datos_generales, respuestas_riesgo, riesgo):
    peso_factor = 0.2
    respuestas_riesgo = convertir_categoricas(respuestas_riesgo)
    valores_numericos = [v for v in respuestas_riesgo.values() if isinstance(v, (int, float))]
    
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
    datos_generales = {"sector": st.selectbox("Sector en el que opera", list(SECTOR_PONDERACION["Riesgo de Endeudamiento"].keys()))}
    
    riesgo = st.selectbox("¿Qué riesgo quieres cuantificar?", list(SECTOR_PONDERACION.keys()))
    respuestas_riesgo = obtener_cuestionario(riesgo)
    
    if st.button("Procesar Información"):
        st.subheader("Paso 4: Procesamiento de Respuestas")
        datos_procesados = procesar_respuestas(datos_generales, respuestas_riesgo, riesgo)
        st.write("Datos procesados:", datos_procesados)

if __name__ == "__main__":
    main()

