import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="VetCare Pro - IA Veterinaria",
    page_icon="🐾",
    layout="wide"
)

# Estilos personalizados
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: bold; color: #1E3A8A; }
    .sub-header { font-size: 1.1rem; color: #4B5563; }
    .stButton button { background-color: #2563EB; color: white; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🐾 VetCare Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Asistente Inteligente de Diagnóstico Veterinario (Powered by Google Gemini)</div>', unsafe_allow_html=True)
st.divider()

# Barra lateral para ingresar la clave de Gemini
with st.sidebar:
    st.header("🔑 Configuración")
    api_key = st.text_input("Ingresa tu Gemini API Key (AIza...):", type="password")
    
    # Intentar leer desde secrets si existe
    if not api_key and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        
    st.info("💡 Obtén tu clave gratis en: [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)")

if not api_key:
    st.warning("👈 Por favor ingresa tu clave API de Google Gemini en el menú lateral para comenzar.")
    st.stop()

# Configurar el cliente de Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Pestañas de funciones
tab1, tab2 = st.tabs(["📝 Historia Clínica", "🩻 Análisis de Radiografía / Imagen"])

# --- TAB 1: HISTORIA CLÍNICA ---
with tab1:
    st.subheader("Análisis de Historia Clínica y Sintomatología")
    
    col1, col2 = st.columns(2)
    with col1:
        especie = st.selectbox("Especie:", ["Canino", "Felino", "Equino", "Bovino", "Exótico", "Otro"])
        raza_edad = st.text_input("Raza y Edad:", placeholder="Ej: Labrador, 5 años")
    with col2:
        peso = st.text_input("Peso (kg):", placeholder="Ej: 22 kg")
        motivo = st.text_input("Motivo de consulta:", placeholder="Ej: Letargo y vómitos desde hace 2 días")

    sintomas = st.text_area("Descripción detallada de síntomas y examen físico:", height=150)

    if st.button("🔍 Analizar Caso Clínico"):
        if not sintomas:
            st.error("Por favor completa la descripción del caso.")
        else:
            with st.spinner("Analizando información clínica con IA..."):
                prompt = f"""
                Actúa como un médico veterinario especialista de alto nivel.
                Analiza el siguiente caso clínico:
                - Especie: {especie}
                - Raza y Edad: {raza_edad}
                - Peso: {peso}
                - Motivo: {motivo}
                - Examen / Síntomas: {sintomas}

                Proporciona un reporte estructurado con:
                1. Posibles Diagnósticos Diferenciales (ordenados por probabilidad).
                2. Pruebas complementarias recomendadas (Análisis de sangre, ecografía, etc.).
                3. Plan de acción o sugerencias terapéuticas iniciales.
                4. Signos de alarma a monitorear.
                """
                try:
                    response = model.generate_content(prompt)
                    st.success("Análisis completado:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error al procesar la solicitud: {e}")

# --- TAB 2: RADIOGRAFÍA / IMAGEN ---
with tab2:
    st.subheader("Análisis de Radiografías o Lesiones Cutáneas")
    
    uploaded_file = st.file_uploader("Sube una imagen o radiografía (JPG, PNG):", type=["jpg", "jpeg", "png"])
    contexto_img = st.text_input("Detalles o sospecha clínica (opcional):", placeholder="Ej: Claudicación en miembro posterior derecho")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen cargada", use_column_width=True)

        if st.button("🩻 Analizar Imagen"):
            with st.spinner("Analizando imagen médica con visión por IA..."):
                prompt_vision = f"""
                Actúa como un radiólogo / dermatólogo veterinario experto.
                Analiza esta imagen médica. Contexto del paciente: {contexto_img if contexto_img else 'No especificado'}.

                Por favor proporciona:
                1. Hallazgos visuales clave observables.
                2. Posibles anomalías o patologías sugeridas por la imagen.
                3. Recomendaciones clínicas adicionales.
                
                Nota: Aclara que este análisis es un soporte de IA y requiere confirmación veterinaria presencial.
                """
                try:
                    response = model.generate_content([prompt_vision, image])
                    st.success("Análisis radiológico / visual completado:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error al analizar la imagen: {e}")
