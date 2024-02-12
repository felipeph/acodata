import streamlit as st

def show_sensor_image(column, image_path):
    with column:
        st.image(image=image_path, use_column_width=True)
    return None