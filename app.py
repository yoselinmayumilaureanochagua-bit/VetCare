import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io
import datetime

# 1. Configuración de la página
st.set_page_config(
    page_title="VetCare Pro | Sistema Clínico & Diagnóstico IA",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilos visuales personalizados (CSS Avanzado)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Fondo principal */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Banner superior */
    .header-container {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 15px -3px rgba(5, 150, 105, 0.2);
    }
    .header-title {
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        color: #FFFFFF !important;
    }
    .header-subtitle {
        font-size: 14px;
        color: #A7F3D0;
        margin-top: 4px;
    }
    
    /* Estilo de Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0F172A;
    }
    section[data-testid="stSidebar"] * {
        color: #F1F5F9 !important;
    }
    
    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #E2E8F0;
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        border-radius: 8px;
        font-weight: 600;
        color: #475569;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #059669 !important;
        color: #FFFFFF !important;
    }
    
    /* Botones primarios */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 12px 20px;
        font-weight: 600;
        font-size: 15px;
        width: 100%;
        box-shadow: 0 4px 6px -1px rgba(5, 150, 105, 0.2);
    }
    
    /* Tarjetas de sección */
    .section-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Encabezado de la App
st.markdown("""
<div class="header-container">
    <div class="header-title">🐾 VetCare Pro</div>
    <div class="header-subtitle">Plataforma de Expediente Clínico y Diagnóstico Por Imagen Veterinaria con IA</div>
</div>
""", unsafe_allow_html=True)

# 4. Barra Lateral (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=70)
    st.markdown("### Configuración del Sistema")
    api_key = st.text_input("OpenAI API Key", type="password", help="Ingresa tu API Key de OpenAI para habilitar las funciones inteligentes.")
    
    st.divider()
    st.markdown("**Datos de la Clínica**")
    clinica_nombre = st.text_input("Nombre de Clínica", "Centro Veterinario VetCare")
    vet_nombre = st.text_input("Veterinario Responsable", "Dr. Alexander V.")
    
    st.divider()
    st.caption("VetCare Pro v2.0 - Desarrollado para asistencia veterinaria profesional.")

# Inicialización de estado de sesión
if 'reporte_ia' not in st.session_state:
    st.session_state.reporte_ia = None

# 5. Pestañas Principales
tab_paciente, tab_examen, tab_radio, tab_informe = st.tabs([
    "📋 1. Paciente & Anamnesis", 
    "🩺 2. Examen Físico", 
    "🦴 3. Radiología IA", 
    "📑 4. Informe & Receta"
])

# --- TAB 1: PACIENTE Y ANAMNESIS ---
with tab_paciente:
    st.markdown("#### 🐶 Información General del Paciente")
    
    col1, col2 = st.columns(2)
    with col1:
        tutor_nombre = st.text_input("Nombre del Tutor", "Carlos Mendoza")
        tutor_dni = st.text_input("DNI / Identificación", "72819304")
        tutor_tel = st.text_input("Teléfono de Contacto", "+51 912 345 678")
    with col2:
        mascota_nombre = st.text_input("Nombre de la Mascota", "Max")
        especie = st.selectbox("Especie", ["Canino", "Felino", "Equino", "Exótico"])
        raza = st.text_input("Raza", "Golden Retriever")
        
    col3, col4, col5 = st.columns(3)
    with col3:
        edad = st.text_input("Edad", "4 años")
    with col4:
        sexo = st.selectbox("Sexo", ["Macho Entero", "Macho Castrado", "Hembra Entera", "Hembra Esterilizada"])
    with col5:
        peso = st.number_input("Peso (kg)", min_value=0.1, value=28.5, step=0.1)

    st.markdown("#### 📝 Motivo de Consulta y Antecedentes")
    motivo = st.text_area("Motivo Principal de Consulta", "Presenta claudicación en miembro posterior derecho desde hace 3 días y decaimiento ligero.")
    antecedentes = st.text_area("Antecedentes Médicos / Enfermedades Previas", "Esquema de vacunación completo. Desparasitado hace 2 meses. Sin alergias conocidas.")

# --- TAB 2: EXAMEN FÍSICO ---
with tab_examen:
    st.markdown("#### 📊 Constantes Fisiológicas")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        temp = st.text_input("Temp (°C)", "38.6")
    with c2:
        fc = st.text_input("FC (ppm)", "110")
    with c3:
        fr = st.text_input("FR (rpm)", "24")
    with c4:
        tllc = st.text_input("TLLC (seg)", "2")

    c5, c6, c7 = st.columns(3)
    with c5:
        mucosas = st.selectbox("Mucosas", ["Rosadas Húmedas", "Pálidas", "Cianóticas", "Ictéricas", "Congestivas"])
    with c6:
        ecc = st.slider("Condición Corporal (1 a 9)", 1, 9, 5)
    with c7:
        hidratacion = st.selectbox("Estado de Hidratación", ["Normal (0-5%)", "Deshidratación Leve (5-7%)", "Deshidratación Moderada (8-10%)", "Severa (>10%)"])

    st.markdown("#### 🔍 Hallazgos en Examen Físico por Sistemas")
    hallazgos = st.text_area("Observaciones del Examen Clínico", "Dolor a la palpación profunda en rodilla derecha. Ligero aumento de volumen articular. Resto de sistemas sin alteración aparente.")

# --- TAB 3: RADIOLOGÍA IA ---
with tab_radio:
    st.markdown("#### 📸 Análisis Inteligente de Radiografía")
    
    uploaded_file = st.file_uploader("Subir imagen radiográfica (JPG, PNG)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Radiografía cargada para estudio", use_container_width=True)

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        region = st.selectbox("Región Anatómica", ["Miembro Posterior", "Miembro Anterior", "Tórax", "Abdomen", "Columna Vertebral", "Cráneo / Mandíbula"])
    with col_r2:
        proyeccion = st.selectbox("Proyección Radiográfica", ["Mediolateral (ML)", "Cranocaudal (CrCa)", "Ventrodorsal (VD)", "Dorsoventral (DV)", "Lateral Izq/Der"])

    sospecha = st.text_input("Sospecha Diagnóstica del Clínico", "Posible rotura de ligamento cruzado o fisura ósea")

    btn_analizar = st.button("✨ Generar Diagnóstico Asistido con IA")

    if btn_analizar:
        if not api_key:
            st.error("⚠️ Requiere una OpenAI API Key. Ingrésala en el menú lateral izquierdo.")
        elif uploaded_file is None:
            st.warning("⚠️ Por favor, sube una imagen de radiografía antes de presionar el botón.")
        else:
            with st.spinner("Procesando radiografía y generando informe asistido..."):
                try:
                    buffered = io.BytesIO()
                    image.save(buffered, format="JPEG")
                    base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    
                    client = OpenAI(api_key=api_key)
                    
                    prompt_profesional = f"""
                    Actúa como un Especialista Diplomado en Radiología Veterinaria.
                    Analiza la imagen adjunta en conjunto con el historial clínico del paciente:

                    DATOS DEL PACIENTE:
                    - Paciente: {mascota_nombre} | Especie: {especie} | Raza: {raza} | Edad: {edad} | Peso: {peso} kg
                    - Constantes: Temp: {temp}°C | FC: {fc} ppm | FR: {fr} rpm | Mucosas: {mucosas}
                    - Motivo y Sintomatología: {motivo}
                    - Hallazgos clínicos: {hallazgos}
                    
                    ESTUDIO RADIOGRÁFICO:
                    - Región: {region}
                    - Proyección: {proyeccion}
                    - Presunción clínica: {sospecha}

                    POR FAVOR PROPORCIONA UN INFORME CON LA SIGUIENTE ESTRUCTURA (Formato Markdown):
                    1. **TÉCNICA Y EVALUACIÓN DE LA IMAGEN**
                    2. **HALLAZGOS RADIOLÓGICOS DETALLADOS**
                    3. **DIAGNÓSTICOS DIFERENCIALES**
                    4. **CONCLUSIÓN DIAGNÓSTICA**
                    5. **SUGERENCIAS DE TRATAMIENTO Y PRÓXIMOS PASOS**

                    *Añade al final una nota aclaratoria indicando que este informe es un soporte de IA y debe ser avalado por el médico veterinario colegiado.*
                    """

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt_profesional},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]
                        }],
                        max_tokens=1200
                    )

                    st.session_state.reporte_ia = response.choices[0].message.content
                    st.success("✅ ¡Análisis completado exitosamente! Consulta los resultados en la pestaña 'Informe & Receta'.")
                except Exception as e:
                    st.error(f"Ocurrió un error en la conexión: {e}")

# --- TAB 4: INFORME Y RECETA ---
with tab_informe:
    st.markdown("#### 📄 Expediente Final y Plan Terapéutico")
    
    fecha_hoy = datetime.date.today().strftime("%d/%m/%Y")
    
    st.info(f"**{clinica_nombre}** | Fecha: {fecha_hoy}\n\n"
            f"**Paciente:** {mascota_nombre} ({especie} - {raza}) | **Tutor:** {tutor_nombre} | **Atendido por:** {vet_nombre}")
    
    st.divider()

    if st.session_state.reporte_ia:
        st.markdown(st.session_state.reporte_ia)
        st.divider()
    else:
        st.warning("Aún no se ha generado un informe de radiología. Puedes ingresar una receta manual o generar el informe en la pestaña anterior.")

    st.markdown("#### 💊 Indicaciones y Receta Médica")
    receta = st.text_area("Prescripción Médica y Tratamiento a Domicilio", 
                         "1. Meloxicam 0.1 mg/kg cada 24 horas por 5 días vía oral con alimento.\n"
                         "2. Reposo relativo por 10 días (evitar saltos y carreras).\n"
                         "3. Aplicación de compresas frías en la zona articular por 10 min 2 veces al día.")
    
    if st.button("🖨️ Generar Resumen Completo"):
        st.success("El resumen de la consulta se encuentra listo para copia o impresión.")
