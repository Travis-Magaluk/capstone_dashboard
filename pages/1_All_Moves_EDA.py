import streamlit as st

import plotly.express as px

conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM all_moves;', ttl="10m")
df.year_move = df.year_move.astype(str)

if 'p_type' not in st.session_state:
    st.session_state['p_type'] = df.lic_type.unique()
    st.session_state.year_move = df.year_move.unique()
    st.session_state.type_moves = df.type_moves.unique()
    st.session_state.dist_vals = (0, 100)


### How can I make this more reusable? Filtering params as a dict with key value pairs.
## Is there a good pandas filtering function where I can input multiple params.

def filter_df(dataframe, year_vals, provider_types, type_moves, dist_vals):
    dataframe = dataframe[dataframe['year_move'].isin(year_vals)]
    dataframe = dataframe[dataframe['lic_type'].isin(provider_types)]
    dataframe = dataframe[dataframe['type_moves'].isin(type_moves)]
    dataframe = dataframe[dataframe['distance_m'] < st.session_state.dist_vals[1]]
    return dataframe


with st.form(key='barchart_params'):
    st.session_state.p_type = st.multiselect('Provider Type',
                                             df.lic_type.unique(), st.session_state.p_type)
    st.session_state.year_move = st.multiselect('Year Move', df.year_move.unique(), st.session_state.year_move)
    st.session_state.type_moves = st.multiselect('Type of Move', df.type_moves.unique(), st.session_state.type_moves)
    st.session_state.dist_vals = st.slider(
        'Select a range of values',
        0.0, 100.0, (25.0, 75.0))
    st.form_submit_button(label='Update Dataframe')

filtered_df = filter_df(df, st.session_state.year_move,
                        st.session_state.p_type, st.session_state.type_moves,
                        st.session_state.dist_vals)

st.write(len(filtered_df))

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
    histplot(filtered_df)

with tab3:
    boxplot(filtered_df)
