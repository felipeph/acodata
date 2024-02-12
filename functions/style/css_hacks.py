import streamlit as st

def remove_streamlit_elements():
    """
    Remove the Streamlit elements of the page that are not desired.
    Uses the CSS hack of the [data-testid=""] elements of the rendered page.
    Internal functions:
        - remove_footer()
        - remove_header()
        - remove_top_padding()
    """
    remove_footer()
    remove_header()
    remove_top_padding()
    return None

def remove_footer():
    st.markdown(
        """
    <style>
        footer {
            display: none;
        }
    </style>
    """,
        unsafe_allow_html=True)
    
def remove_header():
    st.markdown(
        """
    <style>
        [data-testid="stHeader"] {
            display: none
        }
        
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """,
        unsafe_allow_html=True)


def remove_top_padding():
    st.markdown(
        """
 
    <style>
        [data-testid="stAppViewContainer"] {
            top: -160px;
        }
        
    </style>
        
    """,
        unsafe_allow_html=True)
