import streamlit as st
import pandas as pd

# --- Diccionario de datos de las piezas ---
piezas = [
    {"Pieza": "Plato de postre", "Diámetro (cm)": "18–20", "Altura (cm)": "1.5–2", "Proporción": "-", "Volumen": "-", "altura_default": 1.5 ,  "diametro_default": 20 ,},
    {"Pieza": "Plato de taza de café", "Diámetro (cm)": "12–14", "Altura (cm)": "-", "Proporción": "-", "Volumen": "-"},
    {"Pieza": "Plato playo", "Diámetro (cm)": "24–26", "Altura (cm)": "≤ 2.5", "Proporción": "-", "Volumen": "-"},
    {"Pieza": "Plato hondo", "Diámetro (cm)": "22–24", "Altura (cm)": "4–5.5", "Proporción": "1:4 a 1:5", "Volumen": "300–400 ml"},
    {"Pieza": "Taza de café", "Diámetro (cm)": "6–7", "Altura (cm)": "5–6", "Proporción": "1:1", "Volumen": "80–120 ml"},
    {"Pieza": "Taza de té", "Diámetro (cm)": "8–9", "Altura (cm)": "6–7", "Proporción": "1:1.2", "Volumen": "180–220 ml"},
    {"Pieza": "Pocillo (espresso)", "Diámetro (cm)": "5–6", "Altura (cm)": "4–5", "Proporción": "1:1", "Volumen": "50–60 ml"},
    {"Pieza": "Bowl de helado", "Diámetro (cm)": "10–12", "Altura (cm)": "6–7", "Proporción": "1:1", "Volumen": "150–250 ml"},
    {"Pieza": "Tetera para 1", "Diámetro (cm)": "10", "Altura (cm)": "8–10", "Proporción": "boca angosta", "Volumen": "250–300 ml"},
    {"Pieza": "Tetera para 2", "Diámetro (cm)": "12–14", "Altura (cm)": "10–12", "Proporción": "forma bol", "Volumen": "500–600 ml"},
    {"Pieza": "Tetera para 4", "Diámetro (cm)": "16–18", "Altura (cm)": "14–16", "Proporción": "boca más amplia", "Volumen": "900–1200 ml"},
]
opciones = {
    "losa": ("Losa (10%)", 10),
    "gres": ("Gres (25%)", 25),
    "custom": ("Personalizado", None)
}

df_piezas = pd.DataFrame(piezas)
st.title("☕ CeramiCalc")
st.write("Diseñá en crudo. Acertá en cocido.")
col1, col2 = st.columns([2, 1])  # Más espacio para la lista, menos para el input

# En la columna 1: el selectbox
with col1:
    opcion_clave = st.selectbox(
        "Elegí el tipo de material:",
        options=list(opciones.keys()),
        format_func=lambda x: opciones[x][0]
    )
with col2:
    if opcion_clave in ["losa", "gres"]:
        contraccion = opciones[opcion_clave][1]
    else:
        contraccion = st.number_input("% de contracción", min_value=0.0, max_value=100.0, value=12.0)

# --- Selector de pieza ---
opcion = st.selectbox("Seleccioná una pieza de vajilla:", df_piezas["Pieza"].tolist())

# --- Mostrar detalles ---
pieza_sel = df_piezas[df_piezas["Pieza"] == opcion].iloc[0]
st.markdown(f"**Sugerido:** diámetro {pieza_sel['Diámetro (cm)']} cm, altura {pieza_sel['Altura (cm)']} cm")


diametro_default = pieza_sel["diametro_default"]
altura_default = pieza_sel["altura_default"]

# Ingreso de tamaño final deseado
altura_final =st.number_input("Altura deseada (cm)", min_value=0.0, value=altura_default, key="altura")
diametro_final = st.number_input("Diámetro deseado (cm)", min_value=0.0, value=diametro_default, key="diametro")

# Cálculo
altura_cruda = altura_final / (1 - contraccion / 100)

# Resultado
st.markdown("📐 **Tamaño en crudo necesario:**")
st.markdown(f"{altura_cruda:.1f} cm`")


