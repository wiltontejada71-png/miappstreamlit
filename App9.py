import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Configuración de página
st.set_page_config(page_title="App Encuestas BI", layout="wide")

# --- CABECERA GLOBAL ---
def mostrar_cabecera():
    st.markdown("""
        <style>
        .header-container {
            display: flex;
            align-items: center;
            background-color: #f0f2f6;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .header-text {
            flex-grow: 1;
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: #1E3A8A;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 6])
    with col1:
        try:
            st.image("C02_logo_empresa.jpg", width=120)
        except:
            st.info("Logo Empresa")
    with col2:
        st.markdown("<div class='header-text'>Aplicación de Encuesta</div>", unsafe_allow_html=True)

# --- FUNCIONES DE DATOS ---
FILE_PATH = "C03_Encuesta.csv"

def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    else:
        return pd.DataFrame(columns=["PREG1", "PREG2", "PREG3", "PREG4", "PREG5"])

# Definición de preguntas
PREGUNTAS = [
    "¿Qué herramienta de BI utiliza principalmente? (Power BI, Tableau, Excel)",
    "Frecuencia de uso de herramientas BI al día (1 al 5)",
    "Nivel de satisfacción con la calidad de los datos (1 al 5)",
    "¿Considera que BI ha mejorado la toma de decisiones? (Si, No)",
    "Nivel de dificultad para aprender la herramienta (1 al 5)"
]

# --- INTERFAZ PRINCIPAL ---
mostrar_cabecera()

with st.sidebar:
    st.title("📂 Menú de Encuesta")
    menu = st.radio("Seleccione una sección:", 
                    ["Encuesta", "Editar Encuesta", "Respuestas", "Analisis"])
    st.divider()
    st.info("Temática: Uso de herramientas BI en la empresa.")

df = load_data()

# --- SECCIONES ---

if menu == "Encuesta":
    st.subheader("📝 Registro de Nueva Encuesta")
    with st.form("encuesta_form", clear_on_submit=True):
        p1 = st.selectbox(PREGUNTAS[0], ["Power BI", "Tableau", "Excel", "Qlik", "Otros"])
        p2 = st.slider(PREGUNTAS[1], 1, 5, 3)
        p3 = st.slider(PREGUNTAS[2], 1, 5, 3)
        p4 = st.radio(PREGUNTAS[3], ["Si", "No"])
        p5 = st.select_slider(PREGUNTAS[4], options=[1, 2, 3, 4, 5])
        
        submit = st.form_submit_button("Registrar Respuestas")
        
        if submit:
            nueva_data = pd.DataFrame([[p1, p2, p3, p4, p5]], columns=["PREG1", "PREG2", "PREG3", "PREG4", "PREG5"])
            nueva_data.to_csv(FILE_PATH, mode='a', header=not os.path.exists(FILE_PATH), index=False)
            st.success("✅ Encuesta guardada exitosamente.")

elif menu == "Editar Encuesta":
    st.subheader("✏️ Edición de Registros")
    st.write("Modifique los valores directamente en la tabla y presione el botón de abajo.")
    
    # st.data_editor permite editar el CSV como si fuera Excel
    df_edited = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 Guardar Cambios"):
        df_edited.to_csv(FILE_PATH, index=False)
        st.success("Archivo actualizado.")

elif menu == "Respuestas":
    st.subheader("📊 Estadísticas por Pregunta")
    if not df.empty:
        c1, c2 = st.columns(2)
        
        with c1:
            st.write(f"**P1: {PREGUNTAS[0]}**")
            fig1 = px.pie(df, names="PREG1", hole=0.3, color_discrete_sequence=px.colors.qualitative.Safe)
            st.plotly_chart(fig1, use_container_width=True)
            
            st.write(f"**P3: {PREGUNTAS[2]}**")
            fig3 = px.histogram(df, x="PREG3", nbins=5, color_discrete_sequence=['#29b09d'])
            st.plotly_chart(fig3, use_container_width=True)

        with c2:
            st.write(f"**P2: {PREGUNTAS[1]}**")
            fig2 = px.bar(df["PREG2"].value_counts(), title="Distribución de Frecuencia")
            st.plotly_chart(fig2, use_container_width=True)
            
            st.write(f"**P4: {PREGUNTAS[3]}**")
            fig4 = px.funnel_area(names=df["PREG4"].unique(), values=df["PREG4"].value_counts())
            st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning("No hay datos registrados aún.")

elif menu == "Analisis":
    st.subheader("🧪 Análisis de Relaciones")
    if not df.empty:
        st.write("Análisis de Satisfacción vs Dificultad por Herramienta")
        
        # Gráfico de burbujas interactivo
        fig_scatter = px.scatter(df, x="PREG3", y="PREG5", 
                                 size="PREG2", color="PREG1",
                                 hover_name="PREG1", 
                                 labels={"PREG3": "Satisfacción", "PREG5": "Dificultad"},
                                 title="Relación Satisfacción, Dificultad y Frecuencia de Uso")
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Gráfico Solar/Sunburst (Innovador para ver jerarquías)
        st.write("Jerarquía: Herramienta > Mejora Decisiones > Nivel Satisfacción")
        fig_sun = px.sunburst(df, path=['PREG1', 'PREG4', 'PREG3'], values='PREG2')
        st.plotly_chart(fig_sun, use_container_width=True)
    else:

        st.warning("No hay datos para analizar.")
