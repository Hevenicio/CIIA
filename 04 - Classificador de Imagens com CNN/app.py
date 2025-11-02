from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, BatchNormalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing import image
from display_gif import gif  # Adicionado conforme sua atualização
import streamlit as st
from PIL import Image
import numpy as np

# --- Definição das Constantes ---
IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
IMAGE_CHANNELS = 3

# --- Carregamento do Modelo ---
# Esta função cria a arquitetura do modelo exatamete como foi treinada
@st.cache_resource
def create_model():
    model = Sequential()
    
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape = (IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS)))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Dropout(0.25))
    
    model.add(Conv2D(64, (3, 3), activation = 'relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Dropout(0.25))
    
    model.add(Conv2D(128, (3, 3), activation = 'relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Dropout(0.25))
    
    model.add(Flatten())
    model.add(Dense(512, activation = 'relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    
    model.add(Dense(2, activation = 'softmax')) # 2 classes: gato e cachorro
    
    # Compilar o modelo (necessário para carregar pesos, embora não vamos treinar)
    model.compile(loss='categorical_crossentropy', optimizer = 'rmsprop', metrics = ['accuracy'])
    
    return model

# Usamos st.cache_resource para carregar o modelo apenas uma vez
@st.cache_resource
def load_model_weights():
    # Cria a arquitetura
    model = create_model()
    
    # Caminho para o modelo
    model_path = "modelo/model.h5"
    
    # Carrega os pesos salvos
    try:
        model.load_weights(model_path)
        return model
    except Exception as e:
        st.error(f"Erro ao carregar o modelo '{model_path}'. Certifique-se de que o arquivo está nesse caminho. Erro: {e}")
        return None

# Carrega o modelo
model = load_model_weights()

# --- Interface do Streamlit ---
gif("imgs/CNN.gif",) 
st.markdown("<h2 style='text-align: center;'>Classificador de Imagens via CNN: <br>Gato 🐱 ou Cachorro 🐶?</h2>", unsafe_allow_html = True)
st.divider()

# Definição das classes (baseado no notebook, ImageDataGenerator ordena alfabeticamente)
# 'cat' (gato) será 0, 'dog' (cachorro) será 1
class_names = ['Gato', 'Cachorro']

# Uploader de arquivo na sidebar
with st.sidebar:
    st.image('imgs/logo_CIIA.png', use_container_width = True)
    st.markdown("### Faça o upload de uma imagem (jpg, png, jpeg) e o modelo CNN dirá se é um gato ou um cachorro.")
    uploaded_file = st.file_uploader("Escolha uma imagem (jpg, png, jpeg) ...", type = ["jpg", "png", "jpeg"], label_visibility = 'collapsed')

if uploaded_file is not None and model is not None:
    # Ler e exibir a imagem
    try:
        # Abrir a imagem com PIL
        pil_image = Image.open(uploaded_file).convert('RGB')
        
        col1, col2, col3 = st.columns([1, 3, 1])
        # Exibe a imagem carregada na coluna central
        with col2:     
            st.write("") # Espaçamento
            st.image(pil_image, width = 400)
            st.write("") # Espaçamento

        # Botão para classificar na sidebar
        with st.sidebar:    
            if st.button("Classificar Imagem", type = 'primary'):
                with st.spinner("Classificando..."):
                    # --- Pré-processamento da Imagem ---
                    # 1. Redimensionar para o tamanho que o modelo espera (128x128)
                    img_resized = pil_image.resize(IMAGE_SIZE)
                    
                    # 2. Converter para um array numpy
                    img_array = image.img_to_array(img_resized)
                    
                    # 3. Rescalar os pixels (como no `validation_datagen`)
                    img_array = img_array/255.0
                    
                    # 4. Expandir as dimensões para criar um "batch" de 1 imagem
                    # O modelo espera (batch_size, width, height, channels), então (1, 128, 128, 3)
                    img_batch = np.expand_dims(img_array, axis=0)
                    
                    # --- Fazer a Previsão ---
                    prediction = model.predict(img_batch)
                
                with col2:
                    class_index = np.argmax(prediction[0])
                    confidence = np.max(prediction[0])*100
                            
                    # Obter o nome da classe
                    result_class = class_names[class_index]
                            
                    # --- Exibir o Resultado ---
                    emoji = "🐱" if result_class == "Gato" else "🐶"
                    st.success(f"**Resultado:** {result_class} {emoji}")
                    st.write(f"**Confiança:** {confidence:.2f}%")

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar a imagem: {e}")