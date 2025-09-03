import streamlit as st
from PIL import Image
import pytesseract
import numpy as np

st.set_page_config(page_title = 'OCR com PyTesseract', page_icon = '🖼️')

def main():
    '''
        Função principal que constrói a interface do usuário.
    '''
    st.markdown("<h2 style='text-align: center;'>Extrator de textos em Imagem usando PyTesseract 🖼️</h2>", unsafe_allow_html = True)
    st.header('', divider = 'gray')
    
    with st.sidebar:
        st.markdown('# 📤 Envie uma imagem')
        uploaded_file = st.file_uploader('-', type = ['jpg', 'jpeg', 'png'],  help = 'Formatos suportados: JPG, JPEG, PNG', label_visibility = 'collapsed')
        
        # Idioma OCR
        st.markdown('### 🌍 Idioma do OCR')
        idiomas = {'Português': 'por', 'Inglês': 'eng', 'Espanhol': 'spa'}
        lang = st.selectbox('Selecione o idioma:', options = list(idiomas.keys()))
        lang_code = idiomas[lang]

        # Opções de pré-processamento
        st.markdown("### 🔧 Pré-processamento")
        enhance_contrast = st.checkbox('Melhorar contraste', value = True)
        grayscale = st.checkbox('Converter para escala de cinza', value = False)

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            image_array = np.array(image)

            # Aplicar pré-processamento se selecionado
            if enhance_contrast:
                from PIL import ImageEnhance
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(2.0)
                image_array = np.array(image)
            if grayscale:
                image = image.convert("L")

            # Criar duas colunas
            col1, col2 = st.columns(2, border = True)

            with col1:
                st.image(image, use_container_width = True)

            if st.button('Extrair Texto', type = 'primary'):
                with col2:
                    #st.markdown('##### Texto Extraído:')
                    with st.spinner("Extraindo texto da imagem..."):
                        text = pytesseract.image_to_string(image_array, lang = lang_code) # 'por' para português br
                        #st.text(text)
                        text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])

                        st.text_area('##### Texto Extraído:', text, height=200)

                        if text.strip():
                            # Botão para download
                            st.download_button(
                                label = '📥 Baixar Texto',
                                data = text,
                                file_name = f"texto_extraido_{uploaded_file.name.split('.')[0]}.txt",
                                mime = "text/plain",
                                use_container_width = True
                            )
                        else:
                            st.warning('⚠️ Nenhum texto foi encontrado na imagem.')

        except Exception as e:
            st.error(f'Erro: {e}')
            st.write('Por favor, envie um arquivo de imagem válido.')

    # Exemplo de uso
    with st.expander('ℹ️ Como usar esta aplicação'):
            st.markdown("""
            1. **Upload**: Clique em "Browse files" na barra lateral e selecione uma imagem
            2. **Configuração**: Escolha o idioma do texto e opções de pré-processamento
            3. **Extração**: Clique no botão "Extrair Texto" para processar a imagem
            4. **Download**: Baixe o texto extraído como arquivo .txt
            
            **Dicas para melhores resultados:**
            - Use imagens com texto claro e legível
            - Evite imagens muito pequenas ou com baixa resolução
            - Certifique-se de que o texto não está muito inclinado
            - Escolha o idioma correto para melhor precisão
            """)

if __name__ == '__main__':
    main()