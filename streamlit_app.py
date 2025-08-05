import streamlit as st
import pandas as pd
from generar_cono import generar_patron_cono_truncado
from PIL import Image

# --- Diccionario de datos de las piezas ---
piezas = [
    {"Pieza": "Taza de café", "Diámetro (cm)": "6–7", "Altura (cm)": "5–6", "Proporción": "1:1", "Volumen": "80–120 ml", "altura_default": 6, "diametro_default": 7},
    {"Pieza": "Taza de té", "Diámetro (cm)": "8–9", "Altura (cm)": "6–7", "Proporción": "1:1.2", "Volumen": "180–220 ml", "altura_default": 7, "diametro_default": 9},
    {"Pieza": "Pocillo (espresso)", "Diámetro (cm)": "5–6", "Altura (cm)": "4–5", "Proporción": "1:1", "Volumen": "50–60 ml", "altura_default": 5, "diametro_default": 6},
    {"Pieza": "Bowl de helado", "Diámetro (cm)": "10–12", "Altura (cm)": "6–7", "Proporción": "1:1", "Volumen": "150–250 ml", "altura_default": 7, "diametro_default": 12},
    {"Pieza": "Plato de postre", "Diámetro (cm)": "18–20", "Altura (cm)": "1.5–2", "Proporción": "-", "Volumen": "-", "altura_default": 2.0, "diametro_default": 20},
    {"Pieza": "Plato de taza de café", "Diámetro (cm)": "12–14", "Altura (cm)": "-", "Proporción": "-", "Volumen": "-", "altura_default": 0.0, "diametro_default": 14},
    {"Pieza": "Plato playo", "Diámetro (cm)": "24–26", "Altura (cm)": "≤ 2.5", "Proporción": "-", "Volumen": "-", "altura_default": 2.5, "diametro_default": 26},
    {"Pieza": "Plato hondo", "Diámetro (cm)": "22–24", "Altura (cm)": "4–5.5", "Proporción": "1:4 a 1:5", "Volumen": "300–400 ml", "altura_default": 5.5, "diametro_default": 24},
    {"Pieza": "Tetera para 1", "Diámetro (cm)": "10", "Altura (cm)": "8–10", "Proporción": "boca angosta", "Volumen": "250–300 ml", "altura_default": 10, "diametro_default": 10},
    {"Pieza": "Tetera para 2", "Diámetro (cm)": "12–14", "Altura (cm)": "10–12", "Proporción": "forma bol", "Volumen": "500–600 ml", "altura_default": 12, "diametro_default": 14},
    {"Pieza": "Tetera para 4", "Diámetro (cm)": "16–18", "Altura (cm)": "14–16", "Proporción": "boca más amplia", "Volumen": "900–1200 ml", "altura_default": 16, "diametro_default": 18},
]
df_piezas = pd.DataFrame(piezas)

opciones = {
    "losa": ("Losa (10%)", 10),
    "gres": ("Gres (25%)", 25),
    "custom": ("Personalizado", None)
}
def calcular_crudo(valor_cocido, contraccion_porcentual):
    return valor_cocido / (1 - contraccion_porcentual / 100)

st.markdown("""
<h1 style='text-align: center; color: #6e3b3b;'>☕ CeramiCalc</h1>
<p style='text-align: center; font-size:18px;'>Diseñá en crudo. Acertá en cocido.</p>
""", unsafe_allow_html=True)
# st.title("CeramiCalc")
# st.write("Diseñá en crudo. Acertá en cocido.")

tabs = st.tabs(["🧮 Calculadora","📐 Patrones", "📁 Descargables"])

with tabs[0]:  # Calculadora
    col1, col2 = st.columns([2, 1])  # Más espacio para la lista, menos para el input
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

    col_a1, col_a2 = st.columns([1, 1])
    with col_a1:
        altura_final = st.number_input("Altura deseada (cm)", min_value=0.0, value=altura_default, key="altura")
    with col_a2:
        altura_cruda = calcular_crudo(altura_final, contraccion)
        st.markdown(f"→ **{altura_cruda:.1f} cm** en crudo")

    col_d1, col_d2 = st.columns([1, 1])
    with col_d1:
        diametro_final = st.number_input("Diámetro deseado (cm)", min_value=0.0, value=float(diametro_default), key="diametro")
    with col_d2:
        diametro_crudo = calcular_crudo(diametro_final, contraccion)
        st.markdown(f"→ **{diametro_crudo:.1f} cm** en crudo")


with tabs[1]:  
    st.header("Generador de patrón para cono truncado")
    col_b1, col_b2 = st.columns([1, 1])
    with col_b1:
        imagen = Image.open("tazaconica.png")
        st.image(imagen, caption="Cono trucado", use_column_width=True)
    with col_b2:
        with st.form("form_cono"):
            diametro_sup = st.number_input("Diámetro superior (cm)", min_value=1.0, value=8.0)
            diametro_inf = st.number_input("Diámetro inferior (cm)", min_value=1.0, value=6.0)
            altura = st.number_input("Altura del cono truncado (cm)", min_value=1.0, value=9.0)
            submitted = st.form_submit_button("Generar PDF")

        if submitted:
            filename = "patron_cono.pdf"
            generar_patron_cono_truncado(diametro_sup, diametro_inf, altura, filename)
            with open(filename, "rb") as file:
                st.download_button(
                    label="📥 Descargar patrón en PDF",
                    data=file,
                    file_name=filename,
                    mime="application/pdf"
                )

with tabs[2]:
    # Patrones
    st.markdown("### 📂 Patrones descargables")
    st.write("Explorá o descargá los patrones:")

    patrones = [
        {
            "nombre": "Lecherita",
            "descripcion": "Modelo base para armado manual.",
            "link": "https://drive.google.com/uc?export=download&id=1kq17a-WxJRdbhLit7v5UWrJxjQVm-tZr"
        },
        {
            "nombre": "Taza",
            "descripcion": "Modelo con proporciones estándar.",
            "link": "https://drive.google.com/uc?export=download&id=ID_DEL_ARCHIVO_DE_LA_TAZA"
        },
        {
            "nombre": "Florero",
            "descripcion": "Muy pinterest, tamaño mediano.",
            "link": "https://drive.google.com/uc?export=download&id=ID_DEL_ARCHIVO_DEL_CUENCO"
        }
    ]

    for patron in patrones:
        st.markdown(f"""
                     [⬇️ {patron['nombre']}]( {patron['link']} )
         *{patron['descripcion']}* 
        """)

st.markdown("---")  # línea divisoria
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>Hecho por @meludr (meludiazresquin@gmail.com) para Cúprico Taller de Cerámica</p>",
    unsafe_allow_html=True
)