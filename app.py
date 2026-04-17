import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# Configuración de la página
st.set_page_config(page_title="Mi App Educativa", page_icon="🎨")

# 1. Configurar la IA con la clave de los Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Usamos gemini-pro que es el modelo más compatible actualmente
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("⚠️ Falta configurar la clave API en Streamlit Cloud.")

st.title("🎨 Creador de Material para Niños")
st.write("Genera guías, cuentos y resúmenes para niños de 6 a 9 años.")

# Entrada de usuario
tema = st.text_input("¿Qué tema quieres preparar hoy?", placeholder="Ej: Los Símbolos Patrios, El Sistema Solar...")

if st.button("✨ ¡Generar Contenido!"):
    if tema:
        # Instrucción optimizada para niños
        prompt = f"""Actúa como un maestro de primaria experto. 
        Explica el tema '{tema}' para niños de 6 a 9 años. 
        Usa un lenguaje muy sencillo y divertido.
        Divide el texto en: 
        1. Un título llamativo.
        2. Explicación breve (máximo 3 párrafos cortos).
        3. Un dato curioso que empiece con '¿Sabías que...?'.
        No uses palabras difíciles ni tecnicismos."""

        with st.spinner("Escribiendo para los niños..."):
            try:
                response = model.generate_content(prompt)
                texto_final = response.text
                
                st.subheader("Vista previa del material:")
                st.markdown(texto_final)

                # --- GENERACIÓN DEL PDF ---
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                
                # Limpiamos el texto para evitar errores de símbolos extraños en el PDF
                texto_limpio = texto_final.replace('**', '').replace('#', '')
                
                # Escribir el título
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(0, 10, txt="Guia Educativa Personalizada", ln=True, align='C')
                pdf.ln(10)
                
                # Escribir el contenido
                pdf.set_font("Arial", size=12)
                # El encode('latin-1', 'replace') evita que la app falle por tildes
                pdf.multi_cell(0, 10, txt=texto_limpio.encode('latin-1', 'replace').decode('latin-1'))
                
                # Guardar y crear botón de descarga
                nombre_archivo = "guia_educativa.pdf"
                pdf.output(nombre_archivo)
                
                with open(nombre_archivo, "rb") as f:
                    st.download_button(
                        label="📩 Descargar PDF para imprimir",
                        data=f,
                        file_name=f"Guia_{tema}.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Hubo un error al generar: {e}")
    else:
        st.warning("Escribe un tema antes de continuar.")
