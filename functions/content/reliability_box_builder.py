import streamlit as st

import plotly.graph_objects as go

def create_reliability_gauge(reliability):
    """
    Creates a reliability gauge chart.

    Parameters:
    reliability (float): The reliability value between 0 and 1.

    Returns:
    plotly.graph_objects.Figure: The reliability gauge chart.
    """
    # Create a gauge chart
    reliability_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",  # Define o modo do indicador como gráfico de gauge com número
        value = reliability * 100,  # Define o valor do indicador (multiplicando por 100 para exibir como porcentagem)
        domain = {'x': [0, 1], 'y': [0, 1]},  # Define a posição e o tamanho do indicador no layout
        gauge = {'axis': {'range': [None, 100]}}  # Define as configurações do medidor (no eixo de 0 a 100)
        ))
    
    # Atualiza o layout do gráfico
    reliability_gauge.update_layout(
        margin=dict(t=30, b=20, l=40, r=40),  # Define as margens do gráfico
        height=150,  # Define a altura do gráfico
        font=dict(size=16, color="black")  # Define as configurações da fonte
    )
    
    # Define os ticks do eixo do medidor
    reliability_gauge.update_traces(gauge_axis_tickmode="array", selector=dict(type='indicator'))
    reliability_gauge.update_traces(gauge_axis_tickvals=[0,25,50,75,100], selector=dict(type='indicator'))
    
    return reliability_gauge



import streamlit as st

def insert_title(column, title):
    """
    Insert a title into a Streamlit column.

    Parameters:
    column (Streamlit column): The column where the title will be inserted.
    title (str): The title to be inserted.

    Returns:
    None
    """
    if not isinstance(title, str):
        raise TypeError("Title must be a string.")
    
    with column:
        st.markdown(f'<div align="center"><h4>{title}</h4></div>', unsafe_allow_html=True)
    return None

def insert_gauge(column, reliability):
    """
    Insert a reliability gauge chart into a Streamlit column.

    Parameters:
    column (Streamlit column): The column where the gauge chart will be inserted.
    reliability (float): The reliability value between 0 and 1.

    Returns:
    None
    """
    if not isinstance(reliability, (int, float)):
        raise TypeError("Reliability must be a number.")
    if reliability < 0 or reliability > 1:
        raise ValueError("Reliability must be between 0 and 1.")
    
    with column:
        reliability_gauge = create_reliability_gauge(reliability=reliability)
        config = {'staticPlot': True}
        st.plotly_chart(figure_or_data=reliability_gauge, use_container_width=True, config=config)
    return None

def insert_title_and_gauge(column, title, reliability):
    """
    Insert a title followed by a reliability gauge chart into a Streamlit column.

    Parameters:
    column (Streamlit column): The column where the title and gauge chart will be inserted.
    title (str): The title to be inserted.
    reliability (float): The reliability value between 0 and 1.

    Returns:
    None
    """
    if not isinstance(title, str):
        raise TypeError("Title must be a string.")
    
    insert_title(column=column, title=title)
    insert_gauge(column=column, reliability=reliability)
    return None
