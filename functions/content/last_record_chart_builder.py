import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def query_get_variables_from_spot(spot_id, global_data_id_column, global_data_name_column, column_not_null):
    """
    Constructs and returns an SQL query to retrieve variables from a specific spot,
    where the specified column is not null.

    Args:
        spot_id (int): The ID of the spot to retrieve variables for.
        global_data_id_column (str): The name of the column containing the IDs of the global variables.
        global_data_name_column (str): The name of the column containing the names of the global variables.
        column_not_null (str): The name of the column that should be not null.

    Returns:
        str: The SQL query to retrieve the variables.
    """
    query = f"""SELECT {global_data_id_column}, {global_data_name_column}
                FROM spot_{spot_id}_variables
                WHERE {column_not_null} IS NOT NULL;"""
    return query

def query_get_last_record(spot_id, global_data_id):
    """
    Constructs and returns an SQL query to retrieve the last record of a global variable
    from a specific spot.

    Args:
        spot_id (int): The ID of the spot to retrieve the record for.
        global_data_id (int): The ID of the global variable to retrieve the record for.

    Returns:
        str: The SQL query to retrieve the last record.
    """
    query = f"""SELECT *
                FROM spot_{spot_id}_var_{global_data_id}
                ORDER BY timestamp DESC
                LIMIT 1"""
    return query
    

def run_and_time_query(conn, query):
    """
    Executes an SQL query on the database using the provided connection
    and measures the execution time.

    Args:
        conn: The connection to the database.
        query (str): The SQL query to be executed.

    Returns:
        DataFrame: The result of the query as a pandas DataFrame.
        float: The execution time of the query in seconds.
    """
    start_time = time.time()
    query_df = conn.query(query)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return query_df, elapsed_time

def variables_from_spot(conn, spot_id, global_data_id_column, global_data_name_column, column_not_null):
    """
    Returns the variables from a specific spot where the specified column is not null.

    Args:
        conn: The connection to the database.
        spot_id (int): The ID of the spot to retrieve variables for.
        global_data_id_column (str): The name of the column containing the IDs of the global variables.
        global_data_name_column (str): The name of the column containing the names of the global variables.
        column_not_null (str): The name of the column that should be not null.

    Returns:
        DataFrame: A pandas DataFrame containing the variables and their associated IDs.
        float: The execution time of the query in seconds.
    """
    query = query_get_variables_from_spot(spot_id=spot_id,
                                          global_data_id_column=global_data_id_column,
                                          global_data_name_column=global_data_name_column,
                                          column_not_null=column_not_null)
    variables_from_spot_df, elapsed_time = run_and_time_query(conn=conn, query=query)
    return variables_from_spot_df, elapsed_time


def get_last_record(conn, spot_id, global_data_id):
    """
    Returns the last record of a global variable from a specific spot.

    Args:
        conn: The connection to the database.
        spot_id (int): The ID of the spot to retrieve the record for.
        global_data_id (int): The ID of the global variable to retrieve the record for.

    Returns:
        DataFrame: A pandas DataFrame containing the last record of the global variable.
        float: The execution time of the query in seconds.
    """
    query = query_get_last_record(spot_id=spot_id,
                                  global_data_id=global_data_id)
    last_record_df, elapsed_time = run_and_time_query(conn=conn, query=query)
    last_record_df = last_record_df.dropna(axis=1)  # Remove columns with null values
    return last_record_df, elapsed_time

def get_last_record_timestamp(last_record_df):
    """
    Retrieves the timestamp of the last record from a DataFrame and returns it as an integer.

    Parameters:
    - last_record_df (pandas.DataFrame): DataFrame containing the last record.

    Returns:
    - int: Integer representation of the timestamp of the last record.
    """
    last_record_timestamp = last_record_df['timestamp'].iloc[0]
    return int(last_record_timestamp)

def convert_timestamp_to_datetime(timestamp_int):
    """
    Converts an integer timestamp to a datetime object.

    Parameters:
    - timestamp_int (int): Integer representation of the timestamp.

    Returns:
    - datetime.datetime: Datetime object corresponding to the provided timestamp.
    """
    last_record_timestamp_datetime = datetime.fromtimestamp(timestamp_int)
    return last_record_timestamp_datetime

def format_datetime_to_string(timestamp_datetime):
    """
    Formats a datetime object into a string in the format 'YYYY-MM-DD HH:MM:SS'.

    Parameters:
    - datetime_obj (datetime.datetime): The datetime object to be formatted.

    Returns:
    - str: Formatted datetime string in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    timestamp_formated = timestamp_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return timestamp_formated


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
        float: The execution time of the query in seconds.
    """
    query = query_variable_name_alarms(spot_id=spot_id, global_data_id=global_data_id)
    variable_name_alarms_df, elapsed_time = run_and_time_query(conn=conn, query=query)
    return variable_name_alarms_df, elapsed_time

def make_last_record_alarms_df(variable_name_alarms_df, last_record_df):
    """
    Concatenates two DataFrames, removing specific columns, to create a DataFrame suitable for plotting.

    Args:
        variable_name_alarms_df (DataFrame): The DataFrame containing alias name, critical alarm, and alert alarm.
        last_record_df (DataFrame): The DataFrame containing the last record of the global variable.

    Returns:
        DataFrame: A new DataFrame containing the information from both input DataFrames,
                   with specific columns removed for plotting purposes.
    """
    last_record_alarms_df = pd.concat([variable_name_alarms_df, last_record_df], axis=1)
    last_record_alarms_df = last_record_alarms_df.drop(columns=['alias_name', 'timestamp'])
    return last_record_alarms_df

def get_last_record_plot_max_x(last_record_alarms_df):
    """
    Retrieves the maximum value from a DataFrame with only one row.

    Args:
        last_record_plot_df (DataFrame): A DataFrame containing only one row.

    Returns:
        float: The maximum value in the DataFrame.
    """
    last_record_plot_max_x = last_record_alarms_df.max().max()
    return last_record_plot_max_x

def get_last_record_plot_values_df(last_record_df):
    """
    Removes the 'timestamp' column from a DataFrame containing the last record of a global variable.

    Args:
        last_record_df (DataFrame): A DataFrame containing the last record of a global variable.

    Returns:
        DataFrame: A new DataFrame with the 'timestamp' column removed.
    """
    last_record_plot_values_df = last_record_df.drop(columns=['timestamp'])
    
    sorted_columns = sorted(last_record_plot_values_df.columns)

    last_record_plot_values_df = last_record_plot_values_df.reindex(columns=sorted_columns)

    return last_record_plot_values_df

def get_last_record_values_list(last_record_plot_values_df):
    """
    Retrieves the values from a DataFrame with only one row.

    Args:
        last_record_plot_values_df (DataFrame): A DataFrame containing only one row.

    Returns:
        list: A list containing the values of the DataFrame's single row.
    """
    last_record_values_list = last_record_plot_values_df.iloc[0].tolist()
    return last_record_values_list

def get_last_record_variables_list(last_record_plot_values_df):
    last_record_variables_list = last_record_plot_values_df.columns.tolist()
    return last_record_variables_list


def get_last_record_colors_list(last_record_values_list, alarm_critical, alarm_alert):
    """
    Associates values in a list to colors based on specified thresholds.

    Args:
        last_record_values_list (list): A list containing values.
        alarm_critical (float): The threshold value for the critical alarm.
        alarm_alert (float): The threshold value for the alert alarm.

    Returns:
        list: A list of colors associated with each value in the input list.
    """

    last_record_colors_list = []
    for value in last_record_values_list:
        if value > alarm_critical:
            last_record_colors_list.append('red')
        elif value < alarm_alert:
            last_record_colors_list.append('green')
        else:
            last_record_colors_list.append('gold')
    return last_record_colors_list


def create_last_record_plot(last_record_values_list, last_record_variables_alias_list, last_record_colors_list, last_record_plot_max_x, alarm_alert, alarm_critical):
    """
    Creates a last record plot using Plotly.

    Args:
        last_record_values_list (list): List of values to be plotted.
        last_record_variables_alias_list (list): List of variable aliases corresponding to the values.
        last_record_colors_list (list): List of colors corresponding to the values.
        last_record_plot_max_x (float): Maximum x-axis value for the plot.
        alarm_alert (float): Value indicating the alert threshold.
        alarm_critical (float): Value indicating the critical threshold.

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly figure object representing the last record plot.
    """

    fig = go.Figure(go.Bar(
        x=last_record_values_list,
        y=last_record_variables_alias_list,
        orientation='h',
        marker_color=last_record_colors_list,
        text=last_record_values_list,  # Use os valores como texto
        textposition='outside',
        insidetextanchor='end',
        textangle=0,
        texttemplate='%{text:.3f}',# Posicione o texto dentro das barras
    ))
    
    fig.update_xaxes(range=[0, last_record_plot_max_x*1.4])
    
    fig.add_vline(x=alarm_alert, line_dash="dash", line_color="gold")
    fig.add_vline(x=alarm_critical, line_dash="dash", line_color="red")

    fig.update_layout(height=(1+len(last_record_variables_alias_list))*30)
    fig.update_layout(showlegend=False)
    fig.update_layout(margin=dict(t=0, b=0))
    fig.update_layout(font=dict(size=16, color="black"))
    fig.update_layout(yaxis=dict(tickfont=dict(size=16, color="black")))
    
    return fig

def get_text_alias_df(conn):
    text_alias_df = conn.query('SELECT * FROM text_aliases')
    return text_alias_df

def get_new_names(last_record_variables_list, text_alias_df):
    """
    Returns the new names corresponding to the values in the provided list.

    Args:
        last_record_variables_list (list): A list of values.
        text_alias_df (DataFrame): A DataFrame with 'old_name' and 'new_name' columns.

    Returns:
        list: A list of new names corresponding to the provided values.
    """
    
    last_record_df = pd.DataFrame(last_record_variables_list, columns=['old_name'])
    
    last_record_df['index'] = last_record_df.index  # Add numerical index to preserve original order
    
    merged_df = pd.merge(text_alias_df, last_record_df, on='old_name', how='inner')
    
    merged_df = merged_df.sort_values(by='index')  # Sort by numerical index to restore original order
    
    last_record_variables_alias_list = merged_df['new_name'].tolist()
    
    return last_record_variables_alias_list


def show_last_record_chart(column, conn, spot_id_selected):
    """
    Generates and displays last record charts for each global data ID in the provided DataFrame.

    Args:
        column (Streamlit column): Streamlit column to display the charts.
        conn (connection): Database connection.
        variables_from_spot_df (DataFrame): DataFrame containing variables information.
        text_alias_df (DataFrame): DataFrame containing text alias information.
        spot_id_selected (int): Selected spot ID.

    Returns:
        None
    """
    
    text_alias_df = get_text_alias_df(conn=conn)

    variables_from_spot_df, elapsed_time = variables_from_spot(conn=conn,
                                                               spot_id=spot_id_selected,
                                                               global_data_id_column='global_data_id',
                                                               global_data_name_column='global_data_name',
                                                               column_not_null='alarm_critical')

    
    for global_data_id in variables_from_spot_df['global_data_id']:
        variable_name_alarms_df, elapsed_time = get_variable_name_alarms(conn=conn,
                                                                         spot_id=spot_id_selected,
                                                                         global_data_id=global_data_id)
        variable_name = variable_name_alarms_df['alias_name'].iloc[0]

        last_record_df, elapsed_time = get_last_record(conn=conn,
                                                       spot_id=spot_id_selected,
                                                       global_data_id=global_data_id)
        
        last_record_timestamp_int = get_last_record_timestamp(last_record_df=last_record_df)

        last_record_timestamp_datetime = convert_timestamp_to_datetime(last_record_timestamp_int)

        last_record_timestamp_formated = format_datetime_to_string(last_record_timestamp_datetime)
        
        last_record_alarms_df = make_last_record_alarms_df(variable_name_alarms_df=variable_name_alarms_df,
                                                           last_record_df=last_record_df)

        last_record_plot_max_x = get_last_record_plot_max_x(last_record_alarms_df)

        last_record_plot_values_df = get_last_record_plot_values_df(last_record_df=last_record_df)

        last_record_values_list = get_last_record_values_list(last_record_plot_values_df=last_record_plot_values_df)

        last_record_variables_list = get_last_record_variables_list(last_record_plot_values_df=last_record_plot_values_df)

        alarm_critical = last_record_alarms_df['alarm_critical'].iloc[0]

        alarm_alert = last_record_alarms_df['alarm_alert'].iloc[0]

        last_record_color_list = get_last_record_colors_list(last_record_values_list=last_record_values_list,
                                                             alarm_critical=alarm_critical,
                                                             alarm_alert=alarm_alert)
        config = {'staticPlot': True}

        last_record_variables_alias_list = get_new_names(last_record_variables_list=last_record_variables_list,
                                                         text_alias_df=text_alias_df)

        last_record_plot_fig = create_last_record_plot(last_record_values_list=last_record_values_list,
                                                       last_record_variables_alias_list=last_record_variables_alias_list,
                                                       last_record_colors_list=last_record_color_list,
                                                       last_record_plot_max_x=last_record_plot_max_x,
                                                       alarm_critical=alarm_critical,
                                                       alarm_alert=alarm_alert)
        with column:
            st.markdown(f"###### {variable_name}")
            st.plotly_chart(last_record_plot_fig, use_container_width=True, config = config)
    with column:
        st.write(f'Atualizado em: {last_record_timestamp_formated}')        
            
    return last_record_timestamp_int, last_record_timestamp_datetime, variables_from_spot_df 
    
    
