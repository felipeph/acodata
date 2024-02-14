import streamlit as st

def insert_column_title(column, spot_name_selected):
    with column:
        st.markdown(f"#### {spot_name_selected}")
    return None