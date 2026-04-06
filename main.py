import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image

# --- CONFIGURAÇÃO DA API ---
API_KEY = st.secrets.get("GEMINI_API_KEY", "COLE_SUA_CHAVE_AQUI")
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="HRLFARM - Gestão Hospitalar", layout="wide", page_icon="🏥")

# --- FUNÇÃO DE PROCESSAMENTO CORRIGIDA ---
def processar_documento(arquivo):
    # Mudança aqui: usando o nome de modelo mais estável
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = """
    Aja como um farmacêutico clínico. Extraia do documento:
    1. Nome do Paciente (se houver)
    2. Antibióticos/Medicamentos mencionados
    3. Posologia (Dose e Via)
    4. Data de Início ou Tempo de uso.
    Apresente os dados de forma resumida e profissional em Português.
    """
    
    conteudo = arquivo.read()
    if arquivo.type == "application/pdf":
        response = model.generate_content([prompt, {"mime_type": "application/pdf", "data": conteudo}])
    else:
        img = Image.open(arquivo)
        response = model.generate_content([prompt, img])
    
    return response.text

# --- RESTANTE DO CÓDIGO (IGUAL AO ANTERIOR) ---
st.sidebar.title("HRLFARM v1.2")
menu = st.sidebar.radio("Navegação", ["📊 Painel Geral", "📂 Upload Lote (Múltiplos)", "💊 Protocolos Infecto"])

if menu == "📊 Painel Geral":
    st.title("📊 Indicadores da Unidade")
    st.info("Sistema operando normalmente. Aguardando processamento de prontuários.")

elif menu == "📂 Upload Lote (Múltiplos)":
    st.title("📂 Processamento em Lote")
    arquivos_enviados = st.file_uploader("Selecione os prontuários", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if arquivos_enviados:
        if st.button("🚀 Iniciar Processamento de Todos"):
            for arquivo in arquivos_enviados:
                with st.expander(f"📄 Resultado: {arquivo.name}", expanded=True):
                    try:
                        resultado = processar_documento(arquivo)
                        st.markdown(resultado)
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

elif menu == "💊 Protocolos Infecto":
    st.title("🛡️ Suporte Antimicrobiano")
    doenca = st.text_input("Digite a patologia:")
    if st.button("Ver Protocolo"):
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        res = model.generate_content(f"Protocolo de tratamento para {doenca}")
        st.write(res.text)
