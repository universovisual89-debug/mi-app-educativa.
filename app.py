import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# Configuración de la página
st.set_page_config(page_title="Mi App Educativa", page_icon="🎨")

# 1. Configurar la IA con la clave de los Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # CAMBIO IMPORTANTE: Usamos 'gemini-1.5-flash-latest' para evitar el error 404
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("⚠️ Falta configurar la clave API en Streamlit Cloud.")

st.title("🎨 Creador de Material para Niños")
st.write("Genera guías, cuentos y resúmenes para niños de 6 a 9 años.")

# Entrada de usuario
tema = st.text_input("¿Qué tema quieres preparar hoy?", placeholder="Ej: Los Dinosaurios, El Ciclo del Agua...")

if st.button("✨ ¡Generar Contenido!"):
    if tema:
        # Instrucción para la IA
        prompt = f"""Actúa como un maestro de primaria experto. 
        Explica el tema '{tema}' para niños de 6 a 9 años. 
        Usa un lenguaje muy sencillo y divertido.
        Divide el texto en: 
        1. Un título llamativo.
        2. Explicación breve (máximo 3 párrafos cortos).
        3. Un dato curioso que empiece con '¿Sabías que...?'.
        IMPORTANTE: No uses emojis ni símbolos como asteriscos dobles (**)."""

        with st.spinner("Escribiendo para los niños..."):
            try:
                response = model.generate_content(prompt)
                texto_final = response.text
                
                st.subheader("Vista previa del material:")
                st.markdown(texto_final)

                # --- GENERACIÓN DEL PDF ---
                pdf = FPDF()
                pdf.add_page()
                
                # Fuente para el título
                pdf.set_font("Helvetica", 'B', 16)
                pdf.cell(0, 10, txt="Guía Educativa Personalizada", ln=True, align='C')
                pdf.ln(10)
                
                # Limpieza de símbolos Markdown para el PDF
                texto_pdf = texto_final.replace('**', '').replace('#', '').replace('*', '')
                
                # Fuente para el cuerpo del texto
                pdf.set_font("Helvetica", size=12)
                
                # El encode/decode previene errores con tildes y eñes en FPDF
                pdf.multi_cell(0, 10, txt=texto_pdf.encode('latin-1', 'replace').decode('latin-1'))
                
                # Generar el PDF en memoria para descarga directa
                pdf_bytes = pdf.output(dest='S')
                
                st.download_button(
                    label="📩 Descargar PDF para imprimir",
                    data=pdf_bytes,
                    file_name=f"Guia_{tema.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Hubo un error al generar: {e}")
    else:
        st.warning("Escribe un tema antes de continuar.")

