import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configuração
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Chave API ausente.")
    st.stop()

st.set_page_config(page_title="HRLFARM", layout="wide")

# Tabela
if 'pacientes' not in st.session_state:
    st.session_state['pacientes'] = pd.DataFrame(columns=["Paciente", "Medicamento", "Dose", "Frequência", "Status"]).astype(str)

st.title("🏥 HRLFARM - Gestão")

aba_ia, aba_tabela = st.tabs(["🤖 IA", "📝 Tabela"])

with aba_ia:
    arquivos = st.file_uploader("Documentos", type=["pdf", "png", "jpg"], accept_multiple_files=True)
    if arquivos and st.button("Analisar"):
        # Nome exato exigido pelas versões novas
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        for arq in arquivos:
            with st.spinner(f"Lendo {arq.name}..."):
                try:
                    conteudo = arq.read()
                    prompt = "Extraia: Paciente, Medicamento, Dose, Frequência. Não invente dados."
                    response = model.generate_content([prompt, {'mime_type': arq.type, 'data': conteudo}])
                    st.success("Lido com sucesso!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Erro: {e}")

with aba_tabela:
    st.data_editor(st.session_state['pacientes'], num_rows="dynamic", use_container_width=True)
