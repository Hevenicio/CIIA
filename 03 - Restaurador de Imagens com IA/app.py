import streamlit as st
from PIL import Image
import torch
from py_real_esrgan.model import RealESRGAN
from io import BytesIO

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
""", unsafe_allow_html=True)

# --- Funções de Processamento com Cache ---
@st.cache_resource
def carregar_modelo():
    """
    Carrega o modelo Real-ESRGAN. A função é armazenada em cache para
    que o modelo não seja recarregado a cada interação do usuário.
    """
    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = RealESRGAN(device, scale=4)
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
st.set_page_config(layout='centered', page_icon='✨', page_title='Restaurador de Imagens com IA')

# --- Interface Principal ---
st.title('Restaurador de Imagens com IA ✨')
st.write('#### Dê vida nova a fotos antigas, borradas ou de baixa qualidade.')
st.markdown("---")

uploaded_file = st.file_uploader('Selecione uma imagem para restaurar', type=['png', 'jpeg', 'jpg'], label_visibility='collapsed')

# Carrega o modelo de IA
model = carregar_modelo()

if uploaded_file is not None and model is not None:
    if 'file_id' not in st.session_state or st.session_state.file_id != uploaded_file.file_id:
        st.session_state.file_id = uploaded_file.file_id
        st.session_state.restored_image = None

    imagem_original = Image.open(uploaded_file).convert('RGB')
    
    col1, col2 = st.columns(2, border = True)
    with col1:
        # CORREÇÃO APLICADA AQUI
        st.image(imagem_original, width = 'stretch')    

    if st.button('✨ Aplicar Restauração', width = 'stretch', type = 'primary'):
        with st.spinner('A IA está aprimorando a imagem... Por favor, aguarde.'):
            imagem_restaurada = restaurar_imagem(imagem_original, model)
            if imagem_restaurada:
                st.session_state.restored_image = imagem_restaurada

    if st.session_state.restored_image:
        with col2:
            restored_img = st.session_state.restored_image
            # CORREÇÃO APLICADA AQUI
            st.image(restored_img, use_container_width=True)
        
        st.divider()
        st.write('###### **Faça o download da sua imagem restaurada:**')
        
        buf = BytesIO()
        st.session_state.restored_image.save(buf, format = 'PNG')
        byte_im = buf.getvalue()
        
        nome_base = uploaded_file.name.rsplit('.', 1)[0]
        nome_saida = f'{nome_base}_restaurada.png'

        st.download_button(
            label="Baixar em PNG",
            data=byte_im,
            file_name=nome_saida,
            mime="image/png",
            use_container_width=True
        )