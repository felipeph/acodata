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
    spots_df = conn.query(f'SELECT {column} FROM {table};')
    end_time = time.time()
    elapsed_time = end_time - start_time
    return spots_df, elapsed_time


def spot_id_from_alias(df, alias, alias_column, spot_id_column):
    """
    Retrieves the spot_id corresponding to the given alias from a DataFrame.

    Args:
        df (pandas.DataFrame): DataFrame containing the data.
        alias (str): The alias to search for.
        alias_column (str): The name of the column containing aliases.
        spot_id_column (str): The name of the column containing spot_ids.

    Returns:
        int: The spot_id corresponding to the given alias.
    """
    return df.loc[df[alias_column] == alias, spot_id_column].iloc[0]

    

def show_spot_selector(column, title, conn):
    """
    Displays a spot selector and retrieves the selected spot ID.

    This function creates a spot selector using Streamlit and queries the 'alias_spots' table 
    from the database to populate the options. After the user selects a spot, the corresponding 
    spot ID is retrieved.

    Args:
        column (streamlit.delta_generator.DeltaGenerator): Streamlit column object.
        title (str): Title of the spot selector.
        conn: Connection to the database.

    Returns:
        int: The selected spot ID.

    Raises:
        Exception: If an error occurs during the database query.
    """
    with column:        
        insert_title(column=column, title=title)
        try:
            # Retrieve spot options from the database
            spots_df, elapsed_time = get_column_from_table(conn=conn,
                                                            column='*',
                                                            table='alias_spots')
            # Create spot selector
            spot_name_selected = create_spot_selector(column=column,
                                                      label=title,
                                                      options=spots_df['alias'])
            # Retrieve spot ID corresponding to the selected alias
            spot_id_selected = spot_id_from_alias(spots_df,
                                                  alias=spot_name_selected,
                                                  alias_column='alias',
                                                  spot_id_column='spot_id')

            # Display elapsed time for query and selected spot ID
            # st.write(f"Elapsed time for query: {elapsed_time:.6f} seconds")
            # st.success(f"Selected spot: {spot_id_selected}")
            return spot_id_selected, spot_name_selected
        except Exception as e:
            # Display error message if database query fails
            st.error(f"Error querying spots: {e}")
            raise e  # Re-raise the exception to propagate it further if needed

