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
        mode = "gauge+number",
        value = reliability * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, 100]}}
        ))
    reliability_gauge.update_layout(
        margin=dict(t=30, b=20, l=40, r=40),
        height=150,  # Ajuste a altura conforme necessário
        font=dict(size=16, color="black")
    )
    
    reliability_gauge.update_traces(gauge_axis_tickmode="array", selector=dict(type='indicator'))
    
    reliability_gauge.update_traces(gauge_axis_tickvals=[0,25,50,75,100], selector=dict(type='indicator'))
    
    return reliability_gauge