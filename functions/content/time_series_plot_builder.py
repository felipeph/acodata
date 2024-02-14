import streamlit as st
from datetime import datetime, timedelta
import pytz


def insert_column_title(column, spot_name_selected):
    with column:
        st.markdown(f"#### {spot_name_selected}")
    return None

def make_time_selector_columns(column):
    with column:
        col_radio_select, col_date_interval = st.columns(2)
    return col_radio_select, col_date_interval        

def get_time_interval_option(column):
    with column:
        time_interval_option = st.radio(label="Intervalo de tempo",
                                        options=("24 horas", "Personalizado"),
                                        horizontal=True,
                                        label_visibility="collapsed")
    return time_interval_option

def get_default_dates(n_days_ago):
    br_timezone = pytz.timezone('America/Sao_Paulo')
    now_datetime = datetime.now(br_timezone)
    n_days_ago_datetime = now_datetime - timedelta(days=n_days_ago)
    now_date = now_datetime.date()
    n_days_ago_date = n_days_ago_datetime.date()
    return n_days_ago_date, now_date


    

def get_date_interval(column, time_interval_option, default_dates):
    
    if time_interval_option == 'Personalizado':
        with column:
            date_interval = st.date_input(label="Intervalo entre datas", value=default_dates)
    else:
        date_interval = get_default_dates(n_days_ago=1)
    return date_interval
        
    


# def show_time_interval_selector(column):
#     with column:
#         col_radio_select, col_date_interval = st.columns(2)
        
#         with col_radio_select: 
        
#             time_interval_option = st.radio(label="Intervalo de tempo",
#                                             options=("24 horas", "Personalizado"),
#                                             horizontal=True,
#                                             label_visibility="collapsed")
            
#             if time_interval_option == "Personalizado":
#                 with col_date_interval:
#                     date_interval = st.date_input(label="Intervalo entre datas", value=(days_ago_7,today))
                    
                    
                    
                    
                    
                    