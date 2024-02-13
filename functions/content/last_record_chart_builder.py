import time
import pandas as pd

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

