import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

def procesar_respuestas(datos_generales, respuestas_riesgo, riesgo):
    peso_factor = 0.2  # Ajustable según modelo real
    
    # Ahora se cuentan los valores numéricos, incluyendo 0
    valores_numericos = [v for v in respuestas_riesgo.values() if isinstance(v, (int, float))]

    if len(valores_numericos) > 0:
        indice_riesgo = sum(valores_numericos) / len(valores_numericos) * peso_factor
    else:
        indice_riesgo = None  # Si no hay datos, no procesar
    
    return {"riesgo": riesgo, "indice": indice_riesgo}

def main():
    st.title("Herramienta de Cuantificación de Riesgos")
    
    st.subheader("Paso 1: Datos Generales de la Compañía")
    datos_generales = {
        "facturacion": st.number_input("Facturación anual (€)", min_value=0.0, step=10000.0),
        "sociedades": st.number_input("Número de sociedades que participan", min_value=1, step=1),
        "empleados": st.number_input("Número de empleados", min_value=1, step=1),
        "sector": st.selectbox("Sector en el que opera", ["Finanzas", "Energía", "Retail", "Tecnología", "Salud", "Industria", "Otro"]),
        "paises": st.number_input("Número de países en los que opera", min_value=1, step=1),
        "modelo_negocio": st.selectbox("Modelo de negocio", ["B2B", "B2C", "Mixto"]),
        "infraestructura": st.selectbox("Infraestructura tecnológica", ["Baja", "Media", "Alta"]),
        "comercio_digital": st.selectbox("Comercio digital", ["Sí", "No"])
    }
    
    st.subheader("Paso 2: Selección del Riesgo a Cuantificar")
    riesgo = st.selectbox("¿Qué riesgo quieres cuantificar?", ["Riesgo de Liquidez", "Riesgo de Crédito", "Riesgo de Mercado", "Riesgo de Endeudamiento", "Riesgo de Ciberataque"])
    
    st.subheader("Paso 3: Cuestionario Específico del Riesgo")
    respuestas_riesgo = obtener_cuestionario(riesgo)
    
    # Se añade un botón para procesar respuestas
    if st.button("Procesar Información"):
        st.subheader("Paso 4: Procesamiento de Respuestas")
        datos_procesados = procesar_respuestas(datos_generales, respuestas_riesgo, riesgo)
        
        # Solo mostrar el resultado si hay datos válidos
        if datos_procesados["indice"] is not None:
            st.write("Datos procesados:", datos_procesados)
        else:
            st.warning("Por favor, completa al menos un campo del cuestionario antes de procesar.")

if __name__ == "__main__":
    main()
