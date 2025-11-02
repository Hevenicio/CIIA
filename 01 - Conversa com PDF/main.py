from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from custom_css import custom_css  # para ajustes de estilos da interface
from dotenv import load_dotenv
import streamlit as st
import tempfile
import os

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

# --- Configuração da Interface com Streamlit ---
st.markdown(custom_css, unsafe_allow_html = True)

st.set_page_config(
    page_title = '🦜🔗📄 Converse com seu PDF',
    page_icon = '🤖',
    layout = 'centered',
    initial_sidebar_state = 'auto',
    menu_items = None,
)

# --- Função para Processar o PDF e Criar a Cadeia de QA ---
# Usamos cache para que a função não seja reexecutada desnecessariamente
@st.cache_resource
def processar_pdf_e_criar_chain(pdf_file):
    '''Lê o PDF, divide em pedaços, cria embeddings e monta a cadeia de QA.'''
    
    # Salva o arquivo temporariamente para o LangChain poder ler
    with tempfile.NamedTemporaryFile(delete = False, suffix='.pdf') as tmp_file:
        tmp_file.write(pdf_file.getvalue())
        tmp_file_path = tmp_file.name

    # 1. Carregar o PDF
    st.info('Carregando o documento...')
    loader = PyPDFLoader(tmp_file_path)
    documents = loader.load()

    # 2. Dividir o texto em pedaços (chunks)
    st.info('Dividindo o texto em pedaços...')
    text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 100)
    docs = text_splitter.split_documents(documents)

    # 3. Criar embeddings e armazenar no VectorStore (FAISS)
    st.info('Criando o banco de dados vetorial (embeddings)...')
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)

    # 4. Criar a cadeia de busca e resposta
    qa_chain = RetrievalQA.from_chain_type(
        llm = ChatOpenAI(
            model = 'gpt-4o-mini',
            api_key = openai_api_key,
            temperature = .3,), # Adicionando um pouco de criatividade
        chain_type = 'stuff',
        retriever = db.as_retriever()
    )
    
    # Limpa o arquivo temporário
    os.remove(tmp_file_path)
    
    return qa_chain

# --- Interface Principal do App ---
st.markdown("<h2 style='text-align: center;'>🤖 Converse com seus Documentos📄</h2>", unsafe_allow_html=True)
st.header('', divider = 'gray')

# --- Barra Lateral (Sidebar) para Upload ---
with st.sidebar:
    st.header('Faça o Upload')
    uploaded_file = st.file_uploader('Escolha seu arquivo PDF', type = 'pdf', label_visibility = 'collapsed')
    
    if st.button('Processar Documento', disabled = not uploaded_file):
        with st.spinner('Processando... Isso pode levar um momento.'):
            # A função processa o PDF e o resultado (qa_chain) fica em cache
            st.session_state.qa_chain = processar_pdf_e_criar_chain(uploaded_file)
        st.success('Documento processado! Pronto para suas perguntas.')

# --- Lógica do Chat ---
# Inicializa o histórico de mensagens se ele não existir
if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'assistant', 'content': 'Olá! Faça o upload de um PDF na barra lateral e clique em "Processar" para começar.'}]

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Captura a pergunta do usuário
if pergunta := st.chat_input('Faça sua pergunta sobre o documento...'):
    # Adiciona a pergunta do usuário ao histórico e exibe na tela
    st.session_state.messages.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.write(pergunta)

    # Verifica se a cadeia de QA está pronta antes de responder
    if 'qa_chain' in st.session_state:
        # Gera e exibe a resposta do assistente
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                # AQUI ESTÁ A MUDANÇA: Usamos a qa_chain diretamente!
                response_payload = st.session_state.qa_chain.invoke(pergunta)
                resposta = response_payload.get('result', 'Não foi possível encontrar uma resposta.')
                st.write(resposta)

        # Adiciona a resposta do assistente ao histórico
        st.session_state.messages.append({"role": "assistant", "content": resposta})
    else:
        # Mensagem de erro se o PDF não foi processado
        with st.chat_message("assistant"):
            st.warning("Por favor, faça o upload e processe um documento primeiro.")
        st.session_state.messages.append({"role": "assistant", "content": "Desculpe, você precisa primeiro processar um documento na barra lateral."})