import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image

# --- CONFIGURAÇÃO DA API ---
# O segredo é garantir que a API KEY seja lida corretamente
API_KEY = st.secrets.get("GEMINI_API_KEY", "AIzaSyB0sdXSvNdYT464RbbzUCUJu1N4zcIIPVg")
genai.configure(api_key=API_KEY)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="HRLFARM - Gestão", layout="wide", page_icon="🏥")

# --- FUNÇÃO DE PROCESSAMENTO (VERSÃO ESTÁVEL) ---
def processar_documento(arquivo):
    # Usando o nome padrão que funciona em todas as versões
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """
    Aja como um farmacêutico clínico experiente. 
    Analise o documento anexo e extraia:
    1. Identificação do Paciente.
    2. Lista de Antibióticos/Medicamentos.
    3. Posologia completa.
    4. Observações clínicas relevantes.
    Responda em Português de forma estruturada.
    """
    
    # Lê os bytes do arquivo para enviar à API
    doc_bytes = arquivo.read()
    
    if arquivo.type == "application/pdf":
        response = model.generate_content([
            prompt,
            {"mime_type": "application/pdf", "data": doc_bytes}
        ])
    else:
        # Para imagens
        response = model.generate_content([
            prompt,
            {"mime_type": arquivo.type, "data": doc_bytes}
        ])
    
    return response.text

# --- INTERFACE ---
st.title("🏥 HRLFARM - Suporte à Decisão")

st.sidebar.title("Navegação")
menu = st.sidebar.radio("Ir para:", ["Painel", "Processar Prontuários"])

if menu == "Painel":
    st.subheader("Bem-vindo, Leandro!")
    st.write("Selecione 'Processar Prontuários' no menu lateral para começar.")

else:
    st.header("📂 Processamento de Documentos")
    arquivos = st.file_uploader("Suba um ou mais arquivos", type=["pdf", "png", "jpg"], accept_multiple_files=True)
    
    if arquivos and st.button("🚀 Iniciar Análise"):
        for arq in arquivos:
            with st.expander(f"📄 Resultado: {arq.name}", expanded=True):
                try:
                    with st.spinner("IA analisando..."):
                        resultado = processar_documento(arq)
                        st.markdown(resultado)
                except Exception as e:
                    st.error(f"Erro técnico: {str(e)}")
                    st.info("Dica: Verifique se sua API Key nas Secrets é válida.")
