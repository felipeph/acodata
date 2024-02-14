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

    
def get_default_dates(last_record_timestamp_datetime, n_days_ago):
    """
    Calculates the start and end dates for the default interval based on the last record timestamp.

    Parameters:
    - last_record_timestamp_datetime (datetime.datetime): The datetime object representing the timestamp of the last record.
    - n_days_ago (int): The number of days ago from the last record for the default interval.

    Returns:
    - tuple: A tuple containing the start date (n days ago) and end date (last record timestamp date) for the default interval.
    """
    n_days_ago_datetime = last_record_timestamp_datetime - timedelta(days=n_days_ago)
    last_record_timestamp_date = last_record_timestamp_datetime.date()
    
    n_days_ago_date = n_days_ago_datetime.date()
    return n_days_ago_date, last_record_timestamp_date



def get_date_interval(column, time_interval_option, default_dates, last_record_timestamp_datetime):
    """
    Retrieves the date interval selected by the user or defaults to a standard interval.

    Parameters:
    - column (streamlit.delta_generator.DeltaGenerator): The Streamlit column where the date input component will be displayed.
    - time_interval_option (str): The option selected by the user for the time interval.
    - default_dates (tuple): A tuple containing the default dates.
    - last_record_timestamp_datetime (datetime.datetime): The datetime object representing the timestamp of the last record.

    Returns:
    - tuple: A tuple containing the start and end dates of the selected date interval.
    """ 
    if time_interval_option == 'Personalizado':
        with column:
            date_interval = st.date_input(label="Intervalo entre datas", value=default_dates, max_value=default_dates[1])
    else:
        date_interval = get_default_dates(last_record_timestamp_datetime=last_record_timestamp_datetime, 
                                          n_days_ago=1)
    return date_interval
                    
                    
                    
                    