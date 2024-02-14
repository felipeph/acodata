import streamlit as st
from datetime import datetime, timedelta
import pytz


def insert_column_title(column, spot_name_selected):
    """
    Inserts a formatted markdown title inside a Streamlit column.

    Parameters:
    - column (streamlit.delta_generator.DeltaGenerator): The Streamlit column where the title will be inserted.
    - spot_name_selected (str): The name of the selected spot.

    Returns:
    - None
    """
    with column:
        st.markdown(f"#### {spot_name_selected}")
    return None

def make_time_selector_columns(column):
    """
    Creates two columns inside a Streamlit column.

    Parameters:
    - column (streamlit.delta_generator.DeltaGenerator): The Streamlit column where the new columns will be created.

    Returns:
    - tuple: A tuple containing the two created columns.
    """
    with column:
        col_radio_select, col_date_interval = st.columns(2)
    return col_radio_select, col_date_interval        

def get_time_interval_option(column):
    """
    Gets the option selected by the user for the time interval.

    Parameters:
    - column (streamlit.delta_generator.DeltaGenerator): The Streamlit column where the radio selection component will be displayed.

    Returns:
    - str: The option selected by the user.
    """
    with column:
        time_interval_option = st.radio(label="Intervalo de tempo",
                                        options=("24 horas", "Personalizado"),
                                        horizontal=True,
                                        label_visibility="collapsed")
    return time_interval_option

def get_default_dates(n_days_ago):
    """
    Gets the dates for the default interval.

    Parameters:
    - n_days_ago (int): The number of days ago for the default interval.

    Returns:
    - tuple: A tuple containing the dates for the default interval.
    """
    br_timezone = pytz.timezone('America/Sao_Paulo')
    now_datetime = datetime.now(br_timezone)
    n_days_ago_datetime = now_datetime - timedelta(days=n_days_ago)
    now_date = now_datetime.date()
    n_days_ago_date = n_days_ago_datetime.date()
    return n_days_ago_date, now_date
    

def get_date_interval(column, time_interval_option, default_dates):
    """
    Gets the date interval selected by the user.

    Parameters:
    - column (streamlit.delta_generator.DeltaGenerator): The Streamlit column where the date input component will be displayed.
    - time_interval_option (str): The option selected by the user for the time interval.
    - default_dates (tuple): A tuple containing the default dates.

    Returns:
    - tuple: A tuple containing the date interval selected by the user.
    """    
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
                    
                    
                    
                    
                    
                    