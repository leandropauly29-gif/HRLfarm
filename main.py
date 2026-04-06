import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- CONFIGURAÇÃO DA API ---
# Tenta pegar das Secrets do Streamlit, se não encontrar, usa a chave direta
API_KEY = st.secrets.get("GEMINI_API_KEY", "AIzaSyDokYZR8A41mtGEb0xVX4160fY2j0EOyHA")
genai.configure(api_key=API_KEY)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="HRLFARM - Gestão", layout="wide")

# Estilo CSS para deixar com cara de sistema hospitalar
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATERAL ---
st.sidebar.title("🏥 HRLFARM v1.0")
menu = st.sidebar.radio("Navegação", ["Painel Geral", "Upload e Extração", "Protocolos Infecto"])

# --- LÓGICA DO MENU ---

if menu == "Painel Geral":
    st.title("📊 Painel de Controle Farmacêutico")
    st.write("Bem-vindo ao sistema de suporte à decisão do HRL.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Pendências", "12", "+2")
    col2.metric("Intervenções", "05", "-1")
    col3.metric("Alertas", "03", "Novo")

elif menu == "Upload e Extração":
    st.title("📝 Extração de Dados de Prontuário")
    st.info("Suba o PDF ou Foto do prontuário para que a IA organize os dados.")
    
    arquivo = st.file_uploader("Arraste o prontuário aqui", type=["pdf", "png", "jpg", "jpeg"])
    
    if arquivo:
        if st.button("Processar com Gemini Flash"):
            with st.spinner("Analisando prontuário..."):
                try:
                    # Inicializa o modelo
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Se for imagem, processa direto. Se for PDF, avisa que precisa de tratamento.
                    prompt = "Extraia deste prontuário: Nome do paciente, Antibióticos em uso, Dose, e Data de início. Formate como uma tabela."
                    
                    # Simulação de resposta (Para imagens reais, o código enviaria o arquivo)
                    response = model.generate_content([prompt, arquivo] if arquivo.type != "application/pdf" else prompt)
                    
                    st.success("Dados Extraídos!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Erro na API: {e}")

elif menu == "Protocolos Infecto":
    st.title("🛡️ Guia de Antibioticoterapia")
    busca = st.text_input("Busque por patologia ou microrganismo (ex: Sepse, Pseudomonas)")
    
    if busca:
        st.write(f"Sugestões baseadas no protocolo institucional para: **{busca}**")
        st.warning("Lembre-se: Sempre valide com a CCIH local.")
        
        # Aqui o Gemini pode sugerir o protocolo
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Qual o tratamento empírico comum para {busca} em ambiente hospitalar? Responda de forma técnica para farmacêuticos.")
        st.write(res.text)

# --- RODAPÉ ---
st.sidebar.markdown("---")
st.sidebar.write("📍 Paranaguá - PR")
