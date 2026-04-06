import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image

# --- CONFIGURAÇÃO DA API ---
# A chave é buscada primeiro nas Secrets do Streamlit para maior segurança
API_KEY = st.secrets.get("GEMINI_API_KEY", "AIzaSyDokYZR8A41mtGEb0xVX4160fY2j0EOyHA")
genai.configure(api_key=API_KEY)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="HRLFARM - Gestão Hospitalar", layout="wide", page_icon="🏥")

# Estilo visual moderno
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #004a99; color: white; font-weight: bold; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATERAL ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/822/822143.png", width=80)
st.sidebar.title("HRLFARM v1.2")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navegação", ["📊 Painel Geral", "📂 Upload Lote (Múltiplos)", "💊 Protocolos Infecto"])

# --- FUNÇÃO DE PROCESSAMENTO ---
def processar_documento(arquivo):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = """
    Aja como um farmacêutico clínico. Extraia do documento:
    1. Nome do Paciente (se houver)
    2. Antibióticos/Medicamentos mencionados
    3. Posologia (Dose e Via)
    4. Data de Início ou Tempo de uso.
    Apresente os dados de forma resumida e profissional.
    """
    
    if arquivo.type == "application/pdf":
        # Para PDF no Flash, enviamos o texto/arquivo (requer tratamento dependendo da lib)
        # Simplificando para a API processar o conteúdo do arquivo
        response = model.generate_content([prompt, {"mime_type": "application/pdf", "data": arquivo.read()}])
    else:
        # Para imagens (PNG/JPG)
        img = Image.open(arquivo)
        response = model.generate_content([prompt, img])
    
    return response.text

# --- LÓGICA DAS PÁGINAS ---

if menu == "📊 Painel Geral":
    st.title("📊 Indicadores da Unidade")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Leitos Ativos", "45", "Ok")
    col2.metric("Prazos de ATB", "08", "-2")
    col3.metric("Intervenções", "14", "+3")
    col4.metric("Desfechos", "92%", "↑")
    
    st.markdown("---")
    st.subheader("🔔 Alertas Recentes")
    st.warning("Paciente no Leito 204: Tempo de Piperacilina/Tazobactam excedendo 7 dias.")

elif menu == "📂 Upload Lote (Múltiplos)":
    st.title("📂 Processamento em Lote")
    st.info("Selecione vários arquivos (PDF ou Imagem) para extração simultânea.")
    
    # Ativando MULTIPLE=TRUE para permitir vários arquivos
    arquivos_enviados = st.file_uploader(
        "Selecione os prontuários/receitas", 
        type=["pdf", "png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    
    if arquivos_enviados:
        st.write(f"✅ **{len(arquivos_enviados)}** arquivos carregados.")
        
        if st.button("🚀 Iniciar Processamento de Todos"):
            progresso = st.progress(0)
            status_text = st.empty()
            
            for i, arquivo in enumerate(arquivos_enviados):
                # Atualiza barra de progresso
                percentual = (i + 1) / len(arquivos_enviados)
                progresso.progress(percentual)
                status_text.text(f"Processando arquivo {i+1} de {len(arquivos_enviados)}: {arquivo.name}")
                
                with st.expander(f"📄 Resultado: {arquivo.name}", expanded=True):
                    try:
                        resultado = processar_documento(arquivo)
                        st.markdown(resultado)
                    except Exception as e:
                        st.error(f"Erro ao processar {arquivo.name}: {str(e)}")
            
            st.success("🎉 Todos os documentos foram analisados!")
            status_text.text("Concluído!")

elif menu == "💊 Protocolos Infecto":
    st.title("🛡️ Suporte Antimicrobiano")
    st.write("Consulte o protocolo institucional rapidamente.")
    
    doenca = st.selectbox("Selecione a Suspeita Clínica:", 
                         ["Pneumonia Comunitária", "Infecção Urinária (ITU)", "Sepse Foco Abdominal", "Pele e Partes Moles"])
    
    if st.button("Ver Protocolo Sugerido"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Baseado em diretrizes brasileiras de infectologia, qual o esquema empírico inicial para {doenca}?")
        st.info(res.text)

# --- RODAPÉ ---
st.sidebar.markdown("---")
st.sidebar.caption("📍 Farmácia Clínica - Hospital Regional")
st.sidebar.caption("📅 Dados atualizados: 2026")
