# Importing the main packages
import streamlit as st


# Importing customized functions
from functions.style import css_hacks, page_elements 
from functions.content import sticky_logo, header_builder, reliability_box_builder, sensor_image_box_builder, spot_selector_builder, last_record_chart_builder, time_series_plot_builder


# Setting the page configuration
st.set_page_config(page_title='ACOPLAST Brasil',
                   page_icon="images/favicon-acoplast.ico",
                   layout="wide",
                   initial_sidebar_state="collapsed"
                   )

# Database connection to the data functions
conn = st.connection("postgresql", type="sql")

# Removing undesired streamlit elements
css_hacks.remove_streamlit_elements()


# Page skeleton with containers 
banner_logo, header, body = page_elements.create_page_containers()

# Columns of the header container
header_left, header_center, header_right = page_elements.split_container_into_columns(header, [2,2,6], 'medium') 

# Columns of the body container
body_left, body_center, body_right = page_elements.split_container_into_columns(body, [2,2,6], 'medium')


# Inserting the sticky logo banner at the top of the page
sticky_logo.insert_logo(banner_logo)


header_builder.insert_data(col_left=header_left,
                           col_center=header_center,
                           col_right=header_right,
                           client_name='PLATAFORMA CONFIABILIDADE',
                           code='CÓDIGO: 645205 - MODELO: ACOWLV4T4',
                           application='APLICAÇÃO: REDUTORES, MOTOREDUTORES & CONTRA RECUO')

with header:
    st.divider()


reliability_box_builder.insert_title_and_gauge(column=body_left,
                                               title='CONFIABILIDADE',
                                               reliability=0.969)

sensor_image_box_builder.show_sensor_image(column=body_left,
                                           image_path='images/imagem_maquina.png')

spot_id_selected, spot_name_selected = spot_selector_builder.show_spot_selector(column=body_center,
                                                                                title='Pontos de Monitoramento',
                                                                                conn=conn)

last_record_timestamp_int, last_record_timestamp_datetime = last_record_chart_builder.show_last_record_chart(column=body_center,
                                                                                                             conn=conn,
                                                                                                             spot_id_selected=spot_id_selected)


################################################################################
########### TIME_SERIES_PLOT_BUILDER_TESTS #####################################

time_series_plot_builder.insert_column_title(column=body_right,
                                             spot_name_selected=spot_name_selected)

col_radio_select, col_date_interval = time_series_plot_builder.make_time_selector_columns(column=body_right)

time_interval_option = time_series_plot_builder.get_time_interval_option(column=col_radio_select)

n_days_ago_date, last_record_date = time_series_plot_builder.get_default_dates(last_record_timestamp_datetime=last_record_timestamp_datetime, 
                                                                               n_days_ago=7)

date_interval = time_series_plot_builder.get_date_interval(column=col_date_interval,
                                                           time_interval_option=time_interval_option,
                                                           default_dates=(n_days_ago_date, last_record_date),
                                                           last_record_timestamp_datetime = last_record_timestamp_datetime)



with body_right:
    st.write(f'Intervalo de tempo selecionado: {time_interval_option}')
    st.write(f'Datas padrão inicial para pesquisa: {n_days_ago_date, last_record_date}')
    st.write(f'Datas de inicio e fim da análise: {date_interval}')
####################################################################
