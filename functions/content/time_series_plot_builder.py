import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import pytz
import plotly.express as px
from io import BytesIO

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



def get_date_interval(column, time_interval_option, default_dates):
    """
    Retrieves the date interval selected by the user or defaults to a standard interval.

    Parameters:
    - column (streamlit.delta_generator.DeltaGenerator): The Streamlit column where the date input component will be displayed.
    - time_interval_option (str): The option selected by the user for the time interval.
    - default_dates (tuple): A tuple containing the default dates.

    Returns:
    - tuple: A tuple containing the start and end dates of the selected date interval.
    """ 
    if time_interval_option == 'Personalizado':
        with column:
            date_interval = st.date_input(label="Intervalo entre datas", value=default_dates, max_value=default_dates[1])
            return date_interval


def timestamp_from_date_interval(date_interval):
    """
    Converts a date interval into start and end timestamps.

    Parameters:
    - date_interval (tuple): A tuple containing the start and end dates of the interval.

    Returns:
    - tuple: A tuple containing the start and end timestamps.
    """
    start_date_with_minutes = datetime.combine(date_interval[0], datetime.min.time())
    start_timestamp = int(start_date_with_minutes.timestamp())
    end_date_with_minutes = datetime.combine(date_interval[1], datetime.min.time())
    end_timestamp = int(end_date_with_minutes.timestamp())
    return start_timestamp, end_timestamp


def days_to_seconds(n_days):
    """
    Converts a number of days into seconds.

    Parameters:
    - n_days (int): The number of days to be converted.

    Returns:
    - int: The equivalent number of seconds.
    """
    return n_days * 24 * 60 * 60

def get_timestamps_for_query(date_interval, last_record_timestamp_int):
    """
    Calculates the timestamps for the query based on a date interval or the last record timestamp.

    Parameters:
    - date_interval (tuple): A tuple containing the start and end dates of the interval, or None if not provided.
    - last_record_timestamp_int (int): The timestamp of the last record as an integer.

    Returns:
    - tuple: A tuple containing the start and end timestamps for the query.
    """
    if date_interval:
        start_timestamp, end_timestamp = timestamp_from_date_interval(date_interval)
        end_timestamp = end_timestamp + days_to_seconds(1)
    else:
        end_timestamp = last_record_timestamp_int
        start_timestamp = end_timestamp - days_to_seconds(1)
    return start_timestamp, end_timestamp 
                    
                    
def query_interval_timestamps(spot_id, global_data_id, start_timestamp, end_timestamp):
    """
    Constructs a SQL query to retrieve data from a specific spot and global data ID within a given timestamp interval.

    Parameters:
    - spot_id (int): The ID of the spot.
    - global_data_id (int): The ID of the global data.
    - start_timestamp (int): The start timestamp of the interval.
    - end_timestamp (int): The end timestamp of the interval.

    Returns:
    - str: The constructed SQL query.
    """
    query = f"""
            SELECT *
            FROM spot_{spot_id}_var_{global_data_id}
            WHERE timestamp >= {start_timestamp}
            AND timestamp < {end_timestamp}
            """
    return query

def df_from_query(conn, query):
    """
    Retrieves data from the database using the provided connection and SQL query.

    Parameters:
    - conn: The database connection object.
    - query (str): The SQL query to execute.

    Returns:
    - pandas.DataFrame: A DataFrame containing the query results.
    """
    query_df = conn.query(query)
    return query_df

def convert_timestamp_column(df):
    """
    Converts the 'timestamp' column of a DataFrame to the correct datetime format and timezone.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing the 'timestamp' column.

    Returns:
    - pandas.DataFrame: The DataFrame with the 'timestamp' column converted.
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', origin='unix')
    brt_timezone = pytz.timezone('America/Sao_Paulo')
    df['timestamp'] = df['timestamp'].dt.tz_localize(pytz.utc)
    df['timestamp'] = df['timestamp'].dt.tz_convert(brt_timezone)
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)
    return df


def clear_empty_columns(df):
    """
    Removes columns from a DataFrame that contain only NaN values.

    Parameters:
    - df (pandas.DataFrame): The DataFrame to be cleaned.

    Returns:
    - pandas.DataFrame: The cleaned DataFrame.
    """
    clean_df = df.dropna(axis=1, how="all")
    return clean_df

def query_variable_name_alarms(spot_id, global_data_id):
    """
    Constructs and returns an SQL query to retrieve the alias name, critical alarm, and alert alarm
    for a specific spot and global data ID.

    Args:
        spot_id (int): The ID of the spot.
        global_data_id (int): The ID of the global data.

    Returns:
        str: The SQL query to retrieve the alias name, critical alarm, and alert alarm.
    """
    query = f"""SELECT alias_name, alarm_critical, alarm_alert
                FROM alias_variables
                WHERE spot_id = {spot_id}
                  AND global_data_id = {global_data_id};"""
    return query

def get_variable_name_alarms(conn, spot_id, global_data_id):
    """
    Retrieves the alias name, critical alarm, and alert alarm for a specific spot and global data ID.

    Args:
        conn: The connection to the database.
        spot_id (int): The ID of the spot.
        global_data_id (int): The ID of the global data.

    Returns:
        DataFrame: A pandas DataFrame containing the alias name, critical alarm, and alert alarm.
    """
    query = query_variable_name_alarms(spot_id=spot_id, global_data_id=global_data_id)
    variable_name_alarms_df = conn.query(query)
    return variable_name_alarms_df


def get_new_names(variable_data_old_header, text_alias_df):
    """
    Returns the new names corresponding to the values in the provided list.

    Args:
        last_record_variables_list (list): A list of values.
        text_alias_df (DataFrame): A DataFrame with 'old_name' and 'new_name' columns.

    Returns:
        list: A list of new names corresponding to the provided values.
    """
    
    last_record_df = pd.DataFrame(variable_data_old_header, columns=['old_name'])
    
    last_record_df['index'] = last_record_df.index  # Add numerical index to preserve original order
    
    merged_df = pd.merge(text_alias_df, last_record_df, on='old_name', how='inner')
    
    merged_df = merged_df.sort_values(by='index')  # Sort by numerical index to restore original order
    
    variable_data_new_header = merged_df['new_name'].tolist()
    
    return variable_data_new_header

def get_text_alias_df(conn):
    text_alias_df = conn.query('SELECT * FROM text_aliases')
    return text_alias_df


def plot_dataframe_lines(df, variable_name, alarm_alert, alarm_critical):
    columns_list = df.columns.to_list()
    x_column = columns_list[-1]
    y_columns = columns_list[:-1]
    fig = px.line(df, x=x_column, y=y_columns)
    
    fig.add_shape(
        type="line",
        x0=df[x_column].min(),
        x1=df[x_column].max(),
        y0=alarm_alert,
        y1=alarm_alert,
        line=dict(color="orange", dash="dash"),
        name=f'Linha Constante ({alarm_alert})')
    
    fig.add_shape(
        type="line",
        x0=df[x_column].min(),
        x1=df[x_column].max(),
        y0=alarm_critical,
        y1=alarm_critical,
        line=dict(color="red", dash="dash"),
        name=f'Linha Constante ({alarm_critical})')

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        title=""
    ))

    
    fig.update_layout(
        title=variable_name,
        xaxis_title='Data e Hora',
        yaxis_title=variable_name, # Trocar 
        height=250,
    )
    
    fig.update_traces(hovertemplate=None)

    fig.update_layout(hovermode="x unified")
        
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
        )
    )
    
    return fig

def config_to_plot():
    config = {'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['zoom', 'pan', 'autoScale', 'zoomIn', 'zoomOut'],
        }
    return config


def show_line_plots(column, spot_name_selected, last_record_timestamp_datetime, last_record_timestamp_int, variables_from_spot_df, spot_id_selected, conn):
    insert_column_title(column=column, spot_name_selected=spot_name_selected)

    col_radio_select, col_date_interval = make_time_selector_columns(column=column)

    time_interval_option = get_time_interval_option(column=col_radio_select)


    with column:

        n_days_ago_date, last_record_date = get_default_dates(last_record_timestamp_datetime=last_record_timestamp_datetime, 
                                                              n_days_ago=7)

        date_interval = get_date_interval(column=col_date_interval,
                                          time_interval_option=time_interval_option,
                                          default_dates=(n_days_ago_date, last_record_date))


        start_timestamp, end_timestamp = get_timestamps_for_query(date_interval=date_interval,
                                                                  last_record_timestamp_int=last_record_timestamp_int)

        for global_data_id in variables_from_spot_df['global_data_id']:
            query = query_interval_timestamps(spot_id=spot_id_selected,
                                              global_data_id=global_data_id,
                                              start_timestamp=start_timestamp,
                                              end_timestamp=end_timestamp)
            
            variable_data_df = df_from_query(conn=conn, query=query)
            
            variable_data_df = clear_empty_columns(variable_data_df)
            
            variable_data_df = convert_timestamp_column(variable_data_df)
            
            variable_name_alarms_df = get_variable_name_alarms(conn=conn,
                                                               spot_id=spot_id_selected,
                                                               global_data_id= global_data_id)
            
            variable_name = variable_name_alarms_df['alias_name'].iloc[0]
            
            
            alarm_critical = variable_name_alarms_df['alarm_critical'].iloc[0]
            
            alarm_alert = variable_name_alarms_df['alarm_alert'].iloc[0]

            variable_data_old_header = variable_data_df.columns.tolist()
            
            text_alias_df = get_text_alias_df(conn=conn)
            
            variable_data_new_header = get_new_names(variable_data_old_header=variable_data_old_header,
                                                     text_alias_df=text_alias_df)
            
            variable_data_df.columns = variable_data_new_header
            
            
            fig = plot_dataframe_lines(df = variable_data_df,
                                       variable_name=variable_name,
                                       alarm_alert=alarm_alert,
                                       alarm_critical=alarm_critical)
            
            config = config_to_plot()
            
            st.plotly_chart(fig, theme="streamlit", use_container_width=True, config = config)
                        
            with st.expander("Arquivo para Exportação", expanded=False):
                st.dataframe(variable_data_df, use_container_width=True)
                st.download_button(
                    label="Baixar aquivo CSV",
                    data=variable_data_df.to_csv(index=False).encode('utf-8'),
                    file_name=f'{spot_name_selected}_{variable_name}.csv',
                    mime='text/csv',
                )

    return None