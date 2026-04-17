import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# Configuración de la página
st.set_page_config(page_title="Mi App Educativa", page_icon="🎨")

# 1. Configurar la IA con la clave que guardaremos en Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ Falta configurar la clave API en Streamlit Cloud.")

st.title("🎨 Creador de Material para Niños")
st.write("Genera guías, cuentos y resúmenes para niños de 6 a 9 años.")

# Entrada de usuario
tema = st.text_input("¿Qué tema quieres preparar hoy?", placeholder="Ej: Los Símbolos Patrios, El Ciclo del Agua...")

if st.button("✨ ¡Generar Contenido!"):
    if tema:
        # Instrucción para la IA: Lenguaje sencillo y adaptado
        prompt = f"""Actúa como un maestro de primaria experto. 
        Explica el tema '{tema}' para niños de 6 a 9 años. 
        Usa un lenguaje muy sencillo, divertido y con comparaciones fáciles de entender.
        Divide el texto en: 
        1. Un título llamativo.
        2. Explicación breve (máximo 3 párrafos cortos).
        3. Un dato curioso que empiece con '¿Sabías que...?'.
        No uses palabras técnicas complicadas."""

        with st.spinner("Escribiendo para los niños..."):
            try:
                response = model.generate_content(prompt)
                texto_final = response.text
                
                st.subheader("Vista previa del material:")
                st.markdown(texto_final)

                # Generar el PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                # Reemplazamos caracteres especiales para evitar errores en el PDF básico
                texto_pdf = texto_final.replace('•', '-').encode('latin-1', 'ignore').decode('latin-1')
                pdf.multi_cell(0, 10, txt=texto_pdf)
                
                # Botón de descarga
                pdf_output = "guia_educativa.pdf"
                pdf.output(pdf_output)
                with open(pdf_output, "rb") as f:
                    st.download_button("📩 Descargar PDF para imprimir", f, file_name=f"Guia_{tema}.pdf")
            except Exception as e:
                st.error(f"Hubo un error: {e}")
    else:
        st.warning("Por favor, escribe un tema primero.")
