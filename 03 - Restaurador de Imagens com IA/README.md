# 🖼️ Projeto: 

🖼️ Restaurador de Imagens com IA (Real-ESRGAN)Este projeto é uma aplicação web construída com Streamlit que utiliza o modelo de Inteligência Artificial Real-ESRGAN para restaurar e aprimorar a qualidade de imagens. A ferramenta permite que os usuários façam o upload de uma foto antiga, borrada ou de baixa resolução e a transforme em uma imagem nítida e de alta qualidade.🚀 InstalaçãoSiga estes passos para configurar e rodar o projeto em seu ambiente local.1. Pré-requisitosPython 3.10 ou superiorpip e venv2. Clone o RepositórioPrimeiro, clone este repositório para a sua máquina local:git clone [https://github.com/Hevenicio/CIIA.git](https://github.com/Hevenicio/CIIA.git)
cd "CIIA/03 - Restaurador de Imagens com IA"
3. Crie e Ative um Ambiente VirtualÉ uma boa prática criar um ambiente virtual para isolar as dependências do projeto.# Criar o ambiente
python -m venv .upscale_env

# Ativar no Linux/macOS
source .upscale_env/bin/activate

# Ativar no Windows
.\.upscale_env\Scripts\activate
4. Instale as Dependências (Passo Crítico)A instalação do torch pode consumir muita memória. Para evitar problemas, instalaremos os pacotes em duas etapas:a) Instale o PyTorch primeiro:pip install --no-cache-dir torch torchvision
b) Instale o restante das bibliotecas:pip install streamlit pillow py-real-esrgan
5. Baixe o Modelo Pré-treinadoA aplicação precisa do arquivo com os "pesos" do modelo para funcionar.Crie uma pasta chamada weights dentro do diretório do projeto.Baixe o modelo RealESRGAN_x4plus.pth a partir deste link.Mova o arquivo baixado (RealESRGAN_x4plus.pth) para dentro da pasta weights.A estrutura final deve ser:.
├── app_restaurador.py
├── weights/
│   └── RealESRGAN_x4plus.pth
└── ...
▶️ Como Executar a AplicaçãoCom o ambiente virtual ativado e as dependências instaladas, execute o seguinte comando no terminal:streamlit run app_restaurador.py
Seu navegador abrirá automaticamente com a aplicação pronta para ser usada!🛠️ Tecnologias UtilizadasStreamlit: Para a criação da interface web.PyTorch: Framework de base para o modelo de IA.py-real-esrgan: Biblioteca que simplifica o uso do modelo Real-ESRGAN.Pillow: Para manipulação de imagens.



#https://huggingface.co/ai-forever/Real-ESRGAN
#https://github.com/xinntao/Real-ESRGAN
#https://github.com/NeoEagle/Super_Resolution?tab=readme-ov-file
#https://www.youtube.com/watch?v=G-AmeIHpsZE