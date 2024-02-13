import streamlit as st
import time

def query_get_variables_from_spot(spot_id, global_data_id_column, global_data_name_column, column_not_null):
    query = f"""SELECT {global_data_id_column}, {global_data_name_column}
                FROM spot_{spot_id}_variables
                WHERE {column_not_null} IS NOT NULL;"""
    return query
    

def run_and_time_query(conn, query):
    start_time = time.time()
    query_df = conn.query(query)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return query_df, elapsed_time

def variables_from_spot(conn, spot_id, global_data_id_column, global_data_name_column, column_not_null):
    query = query_get_variables_from_spot(spot_id=spot_id,
                                          global_data_id_column=global_data_id_column,
                                          global_data_name_column=global_data_name_column,
                                          column_not_null=column_not_null)
    variables_from_spot_df, elapsed_time = run_and_time_query(conn=conn, query=query)
    return variables_from_spot_df, elapsed_time