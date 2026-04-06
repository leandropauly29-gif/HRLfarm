import streamlit as st
import google.generativeai as genai

# Tenta carregar a chave das Secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Erro: Vá em Settings > Secrets no Streamlit e adicione GEMINI_API_KEY")
    st.stop()

st.set_page_config(page_title="HRLFARM", layout="wide", page_icon="🏥")
st.title("🏥 HRLFARM - Gestão Hospitalar")

arquivos = st.file_uploader("Suba os prontuários (PDF ou Imagem)", type=["pdf", "png", "jpg"], accept_multiple_files=True)

if arquivos and st.button("🚀 Iniciar Análise"):
    # Mudança crucial: Nome completo do modelo
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    for arq in arquivos:
        with st.expander(f"📄 Resultado: {arq.name}", expanded=True):
            try:
                with st.spinner(f"Analisando {arq.name}..."):
                    conteudo = arq.read()
                    prompt = "Você é um farmacêutico hospitalar. Extraia: Paciente, Medicamentos, Dosagem e Data de início. Responda em Português."
                    
                    # Envio formatado para evitar erro 404
                    response = model.generate_content([
                        prompt,
                        {'mime_type': arq.type, 'data': conteudo}
                    ])
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Erro técnico neste arquivo: {e}")
