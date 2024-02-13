import streamlit as st
import time

def insert_title(column, title):
    """
    Inserts a title into the specified column.

    Args:
        column (streamlit.delta_generator.DeltaGenerator): Streamlit column object.
        title (str): Title to be inserted.
    """
    with column:
        st.markdown(f'##### {title}')

def create_spot_selector(column, label, options):
    """
    Creates a spot selector.

    Args:
        column (streamlit.delta_generator.DeltaGenerator): Streamlit column object.
        label (str): Label of the selector.
        options (list): List of options for the selector.

    Returns:
        str: The selected spot.
    """
    with column:
        spot_selected_name = st.radio(label=label,
                                      options=options,
                                      label_visibility="collapsed")
    return spot_selected_name

def get_column_from_table(conn, column, table):
    """
    Gets a column from a table in the database.

    Args:
        conn: Connection to the database.
        column: Name of the column in the table
        table: Name of the table in the database

    Returns:
        pandas.DataFrame: Dataframe containing spot data.
        float: Elapsed time for the database query.
    """
    start_time = time.time()
    spots_df = conn.query(f'SELECT {column} FROM {table};', ttl="10m")
    end_time = time.time()
    elapsed_time = end_time - start_time
    return spots_df, elapsed_time

def get_list_from_column_df(df, column):
    """
    Extracts a list from a column in a dataframe.

    Args:
        df (pandas.DataFrame): Dataframe with the desired column.
        column (str): Name of the column in the Dataframe

    Returns:
        list: List of spot IDs.
    """
    return df[column].tolist()

def show_spot_selector(column, title, conn):
    """
    Displays a spot selector.

    Args:
        column (streamlit.delta_generator.DeltaGenerator): Streamlit column object.
        title (str): Title of the spot selector.
        conn: Connection to the database.

    Returns:
        str: The selected spot.
    """
    
    with column:        
        insert_title(column=column, title=title)
        try:
            spots_df, elapsed_time = get_column_from_table(conn=conn,
                                                        column='spot_id',
                                                        table='spots')
            spots_id_list = get_list_from_column_df(df=spots_df,
                                                    column='spot_id')
            spot_id_selected = create_spot_selector(column=column,
                                                    label=title,
                                                    options=spots_id_list)
            with column:
                st.write(f"Elapsed time for query: {elapsed_time:.6f} seconds")
                st.success(f"Selected spot: {spot_id_selected}")
            return spot_id_selected
        except Exception as e:
            st.error(f"Error querying spots: {e}")
