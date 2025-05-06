import plotly.graph_objects as go

def create_gauge(title, value, min_val=0, max_val=100, unit="°C"):
    mygauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': title},
            gauge={'axis': {'range': [min_val, max_val],
                            'tickmode': 'linear',  # Default is linear
                            'tick0': 0,  # Starting tick
                            'dtick': 10  # Step size (e.g., ticks every 10°C)
                            }},
            number={'suffix': f" {unit}"},
            domain={'x': [0, 1], 'y': [0, 1]}
        )).update_layout(
        margin=dict(t=30, b=30, l=30, r=30),
        height=250  # increase height for better visibility
        )
    return mygauge


