import base64
import streamlit as st

# A abertura da SIDEBAR
st.markdown(
    """
    <style>
        /* Aumenta a largura da sidebar */
        [data-testid="stSidebar"] {
            width: 250px;        /* largura padrão ~250px */
            min-width: 250px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def gif(caminho: str, largura: int = 530, altura: int = 320):
    """Exibe um GIF com cantos arredondados e sombra no Streamlit."""
    try:
        with open(caminho, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode("utf-8")
        html = f"""
        <div style="display: flex; justify-content: center;">
            <img src="data:image/gif;base64,{b64}"
                 width="{largura}"
                 style="
                    border-radius: 25px;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.25);
                    border: 2px solid #f0f0f0;
                 ">
        </div>
        """
        st.components.v1.html(html, height = altura)
    except FileNotFoundError:
        st.warning(f"❌ Arquivo não encontrado: {caminho}")

