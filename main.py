import streamlit as st
import google.generativeai as genai

# Configuração robusta da API
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Configure a GEMINI_API_KEY nas Secrets do Streamlit!")
    st.stop()

st.set_page_config(page_title="HRLFARM", layout="wide")
st.title("🏥 HRLFARM - Suporte à Decisão")

arquivos = st.file_uploader("Suba os prontuários (PDF ou Imagem)", type=["pdf", "png", "jpg"], accept_multiple_files=True)

if arquivos and st.button("🚀 Iniciar Análise"):
    # Usando o nome completo do modelo para evitar o erro 404
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
    
    for arq in arquivos:
        with st.expander(f"📄 Resultado: {arq.name}", expanded=True):
            try:
                with st.spinner("IA analisando documento..."):
                    conteudo = arq.read()
                    prompt = "Você é um farmacêutico hospitalar. Extraia: Paciente, Medicamentos, Dosagem e Data."
                    
                    # Formato de envio compatível
                    response = model.generate_content([
                        prompt,
                        {'mime_type': arq.type, 'data': conteudo}
                    ])
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Erro técnico: {e}")
