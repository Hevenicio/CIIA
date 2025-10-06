from streamlit_image_comparison import image_comparison
from py_real_esrgan.model import RealESRGAN
import streamlit as st
from io import BytesIO
from PIL import Image
import torch

# --- CSS Simples para Estilizar o Uploader ---
st.markdown("""
    <style>
        .st-emotion-cache-1jicfl2 {
            border: 2px dashed #a8a8a8;
            padding: 2rem;
            border-radius: 0.5rem;
            text-align: center;
        }
        .st-emotion-cache-1jicfl2:hover {
            border-color: #f8f9fa;
        }
    </style>
""", unsafe_allow_html = True)

# --- Funções de Processamento com Cache ---
@st.cache_resource
def carregar_modelo():
    """
    Carrega o modelo Real-ESRGAN. A função é armazenada em cache para
    que o modelo não seja recarregado a cada interação do usuário.
    """
    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = RealESRGAN(device, scale = 4)
        model_path = 'modelo/RealESRGAN_x4plus.pth'
        model.load_weights(model_path)
        return model
    except FileNotFoundError:
        st.error("Arquivo do modelo não encontrado! Certifique-se de que 'RealESRGAN_x4plus.pth' está na pasta 'modelo'.")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar o modelo: {e}")
        return None

def restaurar_imagem(imagem_pil, model):
    """
    Recebe uma imagem (formato PIL), a aprimora usando o modelo e a retorna.
    """
    if model is None:
        return None
    try:
        sr_image = model.predict(imagem_pil)
        return sr_image
    except Exception as e:
        st.error(f"Ocorreu um erro durante o processamento da imagem: {e}")
        return None

# --- Configuração da Página ---
st.set_page_config(layout = 'centered', page_icon = '✨🖼️', page_title = 'Restaurador de Imagens com IA')

# --- Interface Principal ---
st.markdown("<h2 style='text-align: center;'>Restaurador de Imagens com IA ✨🖼️</h2>", unsafe_allow_html = True)
st.markdown("<h5 style='text-align: center;'>Dê vida nova a fotos antigas, borradas ou de baixa qualidade.</h5>", unsafe_allow_html = True)
st.markdown("---")


# Carrega o modelo de IA
model = carregar_modelo()

with st.sidebar:
    #st.logo('img/logo_CIIA.png', size = 'large', )
    st.image('img/logo_CIIA.png', use_container_width = True)

    st.markdown('# 📤 Envie uma imagem')
    #uploaded_file = st.file_uploader('-', type = ['jpg', 'jpeg', 'png'],  help = 'Formatos suportados: JPG, JPEG, PNG', label_visibility = 'collapsed')
    uploaded_file = st.file_uploader('Selecione uma imagem para restaurar', type = ['png', 'jpeg', 'jpg'], label_visibility = 'collapsed')


if uploaded_file is not None and model is not None:
    if 'file_id' not in st.session_state or st.session_state.file_id != uploaded_file.file_id:
        st.session_state.file_id = uploaded_file.file_id
        st.session_state.restored_image = None

    imagem_original = Image.open(uploaded_file).convert('RGB')

    # Botão de restauração fica visível o tempo todo
    if st.sidebar.button('✨ Aplicar Restauração', width = 'content', type = 'primary'):
        with st.spinner('A image está sendo aprimorada... Por favor, aguarde.'):
            imagem_restaurada = restaurar_imagem(imagem_original, model)
            if imagem_restaurada:
                st.session_state.restored_image = imagem_restaurada

    # Lógica de exibição condicional
    if st.session_state.restored_image is None:
        # Se AINDA NÃO restaurou, mostra só a original
        st.sidebar.image(imagem_original, width = 'content', use_container_width = True)
    else:
        image_comparison(
            img1 = imagem_original,
            img2 = st.session_state.restored_image,
            label1 = 'Original',
            label2 = 'Restaurada',
            width = 700,
            starting_position = 50,
            show_labels = True,
            make_responsive = True,
            in_memory = True,
        )

        st.divider()

        buf = BytesIO()
        st.session_state.restored_image.save(buf, format = "PNG")
        byte_im = buf.getvalue()

        nome_base = uploaded_file.name.rsplit('.', 1)[0]
        nome_saida = f'{nome_base}_restaurada.png'

        st.sidebar.write('###### **Faça o download da imagem restaurada:**')
        st.sidebar.download_button(
            label = "Baixar em PNG",
            data = byte_im,
            file_name = nome_saida,
            mime = "image/png",
            width = 'content'
        )