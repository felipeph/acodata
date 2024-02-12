import streamlit as st

def insert_acodata_one(column):
    """
    Inserts the ACOdata® logo and tagline into the specified column.

    Parameters:
    column (streamlit.container): The column where the logo and tagline will be inserted.

    Returns:
    None
    """
    with column:
        st.markdown(f'<div align="center"><h1 style="color:#2A4B80; display: inline;"><span style="font-size: 1em;">ACODATA®</span><span style="font-size: 0.6em;">one</span></h1><h5 style="color:#2A4B80; ">MONITORAMENTO DE ATIVOS</h5></div>', unsafe_allow_html=True)
    return None

def insert_client_name(column, client_name):
    """
    Inserts the client's name into the specified column.

    Parameters:
    column (streamlit.container): The column where the client's name will be inserted.
    client_name (str): The name of the client.

    Returns:
    None
    """
    with column:
        st.markdown(f'<div align="center"><h2>{client_name}</h2>', unsafe_allow_html=True)
    return None

def insert_code_application(column, code, application):
    """
    Inserts the code and application name into the specified column.

    Parameters:
    column (streamlit.container): The column where the code and application name will be inserted.
    code (str): The code of the application.
    application (str): The name of the application.

    Returns:
    None
    """
    with column:
        st.markdown(f'<h5 style="color:#2A4B80; ">{code}</h5>', unsafe_allow_html=True)
        st.markdown(f'<h5 style="color:#2A4B80; ">{application}</h5>', unsafe_allow_html=True)
    return None

def insert_data(col_left, col_center, col_right, client_name, code, application):
    """
    Inserts the ACOdata® logo, client's name, code, and application name into the specified columns.

    Parameters:
    col_left (streamlit.container): The column for the ACOdata® logo.
    col_center (streamlit.container): The column for the client's name.
    col_right (streamlit.container): The column for the code and application name.
    client_name (str): The name of the client.
    code (str): The code of the application.
    application (str): The name of the application.

    Returns:
    None
    """
    insert_acodata_one(col_left)
    insert_client_name(col_center, client_name)
    insert_code_application(col_right, code, application)
    return None
