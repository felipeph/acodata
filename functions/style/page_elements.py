import streamlit as st

def create_page_containers():
    """
    Creates containers for the banner/logo, header, and main body of the page.

    Returns:
    tuple: A tuple containing the created containers (banner_logo, header, body).
    """
    # Container for the banner/logo
    banner_logo = st.container()

    # Container for the header
    header = st.container()

    # Container for the main body of the page
    body = st.container()
    
    return banner_logo, header, body

def split_container_into_columns(container, column_width, gap):
    """
    Splits a container into columns.

    Args:
    container: Streamlit container object.
    column_width (list): List containing the widths of each column.
    gap (str): Gap between columns ('small', 'medium', 'large').

    Returns:
    tuple: A tuple containing the created columns (col_left, col_center, col_right).
    """
    with container:
        # Splitting the container into columns: one for each part of the header
        col_left, col_center, col_right = container.columns(column_width, gap=gap)
    
    return col_left, col_center, col_right

