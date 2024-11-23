# -*- coding: utf-8 -*-
"""solemne-tres.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iZHF2aocIHF2acU7hYf1uIJAxQaQAf-A
"""
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
# Función para obtener datos de la API REST Countries
def obtener_datos_api():
    url = "https://restcountries.com/v3.1/all"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json()
    else:
        st.error(f"Error al obtener datos de la API. Código de estado: {respuesta.status_code}")
        return None

# Función para procesar datos y convertirlos en un DataFrame
def procesar_datos(datos):
    columnas = ["Nombre", "Región", "Población", "Área", "Idiomas"]
    filas = []

    for pais in datos:
        nombre = pais.get("name", {}).get("common", "N/A")
        region = pais.get("region", "N/A")
        poblacion = pais.get("population", 0)
        area = pais.get("area", None)
        idiomas = ", ".join(pais.get("languages", {}).values()) if "languages" in pais else "N/A"

        filas.append([nombre, region, poblacion, area, idiomas])

    df = pd.DataFrame(filas, columns=columnas)
    return df

# Función para generar gráficos

def generar_graficos(df):
    fig, ax = plt.subplots(2, 1, figsize=(10, 10))

    # Gráfico de Población por Región
    poblacion_por_region = df.groupby("Región")["Población"].sum().sort_values(ascending=False)
    poblacion_por_region.plot(kind="bar", ax=ax[0], color="skyblue")
    ax[0].set_title("Población por Región")
    ax[0].set_ylabel("Población")

    # Gráfico de los 10 países más grandes en área
    mayores_paises = df.nlargest(10, "Área")
    mayores_paises.plot(kind="bar", x="Nombre", y="Área", ax=ax[1], color="green")
    ax[1].set_title("Top 10 países por área")
    ax[1].set_ylabel("Área (km²)")

    plt.tight_layout()
    st.pyplot(fig)

# Aplicación principal en Streamlit
def main():
    st.title("Análisis de Datos de Países - API REST Countries")

    # Obtener datos de la API
    datos = obtener_datos_api()

    if datos:
        # Procesar datos
        df = procesar_datos(datos)
        st.subheader("Datos de Países")
        st.dataframe(df)

        # Seleccionar región para análisis
        regiones = df["Región"].dropna().unique()
        region_seleccionada = st.selectbox("Selecciona una Región", regiones)

        df_filtrado = df[df["Región"] == region_seleccionada]
        st.write(f"Mostrando datos para la región: {region_seleccionada}")
        st.dataframe(df_filtrado)

        # Generar gráficos
        st.subheader("Visualización de Datos")
        generar_graficos(df_filtrado)

if __name__ == "__main__":
    main()
