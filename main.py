import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- 1. CONFIGURAÇÃO E SEGURANÇA ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Chave API não encontrada nas Secrets.")
    st.stop()

st.set_page_config(page_title="HRLFARM - Gestão", layout="wide", page_icon="🏥")

# --- 2. BANCO DE DADOS VIRTUAL (SESSÃO) ---
# Cria a tabela forçando o tipo texto (string) para evitar o ArrowTypeError
if 'pacientes' not in st.session_state:
    st.session_state['pacientes'] = pd.DataFrame(
        columns=["Paciente", "Medicamento", "Dose", "Frequência", "Status"]
    ).astype(str)

# --- 3. FUNÇÃO DE EXTRAÇÃO (SEM ALUCINAÇÃO) ---
def extrair_dados_ia(arquivo):
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    prompt = """
    Você é um auditor farmacêutico rigoroso.
    REGRA 1: Leia o documento anexado.
    REGRA 2: EXTRAIA APENAS o que está escrito. NUNCA invente nomes, pacientes ou medicamentos.
    REGRA 3: Se o documento estiver em branco, borrado ou ilegível, responda APENAS: "ERRO: ILEGÍVEL".
    Extraia e liste: Paciente, Medicamento, Dose e Frequência.
    """
    
    conteudo = arquivo.read()
    response = model.generate_content([
        prompt,
        {'mime_type': arquivo.type, 'data': conteudo}
    ])
    return response.text

# --- 4. INTERFACE E MENUS ---
st.title("🏥 HRLFARM - Gestão de Pacientes")

aba_ia, aba_tabela = st.tabs(["🤖 Extração por IA", "📝 Edição e Inserção Manual"])

with aba_ia:
    st.subheader("Suba a Prescrição para Leitura")
    arquivos = st.file_uploader("Documentos", type=["pdf", "png", "jpg"], accept_multiple_files=True)
    
    if arquivos and st.button("Analisar Documentos"):
        for arq in arquivos:
            with st.expander(f"Resultado: {arq.name}", expanded=True):
                with st.spinner("Lendo documento..."):
                    try:
                        resultado = extrair_dados_ia(arq)
                        st.markdown(resultado)
                        st.info("💡 Vá para a aba 'Edição Manual' para registrar ou corrigir estes dados na planilha.")
                    except Exception as e:
                        st.error(f"Falha na leitura do arquivo: {e}")

with aba_tabela:
    st.subheader("📋 Banco de Pacientes Ativos")
    st.write("Clique nas células para **editar** ou role até a última linha vazia para **adicionar** novos pacientes manualmente.")
    
    # MÁGICA AQUI: Configurando as colunas para evitar o erro e adicionar Dropdown
    tabela_editada = st.data_editor(
        st.session_state['pacientes'],
        num_rows="dynamic",
        use_container_width=True,
        key="editor_tabela",
        column_config={
            "Paciente": st.column_config.TextColumn("Nome do Paciente", required=True),
            "Medicamento": st.column_config.TextColumn("Antimicrobiano/Medicamento"),
            "Dose": st.column_config.TextColumn("Dose (ex: 500mg, 4.5g)"),
            "Frequência": st.column_config.TextColumn("Frequência (ex: 8/8h)"),
            "Status": st.column_config.SelectboxColumn(
                "Status Clínico",
                help="Selecione o status do tratamento",
                options=["Ativo", "Alta", "Suspenso", "Óbito"],
                required=True
            )
        }
    )
    
    st.session_state['pacientes'] = tabela_editada
    
    if st.button("💾 Salvar Alterações Temporárias"):
        st.success("Tabela atualizada com sucesso!")
