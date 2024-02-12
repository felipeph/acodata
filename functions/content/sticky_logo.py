import streamlit as st

def insert_logo(container):
    """
    Inserts the logo image and makes it sticky at the top of the page.

    Parameters:
    container (streamlit.container): The container where the logo will be inserted.

    Returns:
    None
    """
    with container:
        st.markdown(f'<div align="center"><img src="https://www.acoplastbrasil.com.br/wp-content/uploads/2018/12/logo_acoplast.png" alt="Logo Acoplast Brasil" style="width: 250px; height: auto;"></div>', unsafe_allow_html=True)
        st.markdown("""<div class='fixed-header'/>""", unsafe_allow_html=True)
        make_logo_sticky()
    

def make_logo_sticky():
    """
    Makes the logo sticky at the top of the page using CSS hack.

    Returns:
    None
    """
    st.markdown(
    """
        <style>
            div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
                position: sticky;
                /*top: 0rem;*/
                top: 160px;
                background-color: white;
                z-index: 999;
            }
            .fixed-header {
                border-bottom: 1px solid #2A4B80;
            }
        </style>
    """,
    unsafe_allow_html=True
)