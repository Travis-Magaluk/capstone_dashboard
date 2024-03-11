import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.title("EDA of AutoTrader Data")
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM all_moves;', ttl="10m")

plot_options = ["Histogram", "Boxplot"]
continuous_cols = ["distance_m"]
other_cols = ['lic_type', 'year_move', 'type_moves', 'move_numbe']
tab2, tab3 = st.tabs(plot_options)


def histplot(df):

    hist_col = st.selectbox("Select x-axis data", options=other_cols, key=8)
    if hist_col in continuous_cols:
        nbins = st.slider("nbins", min_value=5, max_value=30)
    else:
        nbins = None
    st.markdown("Click on the legend to (add/remove makes)")

    plot = px.histogram(df, x=hist_col, nbins=nbins)
    st.plotly_chart(plot, use_container_width=True)


def boxplot(df):

    x_axis_label = st.selectbox("Select x-axis data", options=other_cols, key=11)

    st.markdown("Click on the legend to (add/remove makes)")

    plot = px.box(df, x=x_axis_label, y='distance_m')
    st.plotly_chart(plot, use_container_width=True)

with tab2:
    histplot(df)

with tab3:
    boxplot(df)