import streamlit as st
import time 
st.set_page_config(
    page_title="Teste de Conexão Streamlit-Postgres",
    page_icon="⏳",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('Teste de conexão com banco de dados')

conn = st.connection("postgresql", type="sql")

start_time = time.time()
spots_df = conn.query('SELECT * FROM spots;', ttl="10m")
end_time = time.time()
elapsed_time = end_time - start_time
st.subheader('Lista de Spots')
st.dataframe(spots_df, use_container_width=True)
st.write(f'Tempo de execução: {elapsed_time}')

for spot in spots_df['spot_id']:
    start_time = time.time()
    spot_variables_df = conn.query(f'SELECT * FROM spot_{spot}_variables;', ttl="10m")
    end_time = time.time()
    elapsed_time = end_time - start_time
    spot_variables_df = spot_variables_df[spot_variables_df['alarm_critical'].notna()]
    st.subheader(f'Lista de Variáveis do Spot {spot}')
    st.dataframe(spot_variables_df, use_container_width=True)
    st.write(f'Tempo de execução: {elapsed_time}')
    
    for variable in spot_variables_df['global_data_id']:
        start_time = time.time()
        spot_variables_df = conn.query(f'SELECT * FROM spot_{spot}_var_{variable};', ttl="10m")
        end_time = time.time()
        elapsed_time = end_time - start_time
        st.subheader(f'Dados da variável {variable} do spot {spot}')
        st.dataframe(spot_variables_df, use_container_width=True)
        st.write(f'Tempo de execução: {elapsed_time}')
