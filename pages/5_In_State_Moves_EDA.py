import streamlit as st

import plotly.express as px
st.set_page_config(layout="wide")
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM provider_moves;', ttl="10m")
df.year_move = df.year_move.astype(str)

st.write(df.head())

if 'p_type' not in st.session_state:
    st.session_state['p_type'] = df.provider_t.unique()
    st.session_state.year_move = df.year_move.unique()
    st.session_state.dist_vals = (0, 100)


### How can I make this more reusable? Filtering params as a dict with key value pairs.
## Is there a good pandas filtering function where I can input multiple params.

def filter_df(dataframe, year_vals, provider_types, dist_vals):
    dataframe = dataframe[dataframe['year_move'].isin(year_vals)]
    dataframe = dataframe[dataframe['provider_t'].isin(provider_types)]
    dataframe = dataframe[dataframe['distance_m'] < st.session_state.dist_vals[1]]
    dataframe = dataframe[dataframe['distance_m'] > st.session_state.dist_vals[0]]
    return dataframe


def histplot(df):
    hist_col = st.selectbox("Select x-axis data", options=other_cols, key=8)
    if hist_col in continuous_cols:
        nbins = st.slider("nbins", min_value=5, max_value=30)
    else:
        nbins = None
    st.markdown("Some text about the selection above.")

    plot = px.histogram(df, x=hist_col, nbins=nbins)
    st.plotly_chart(plot)


def boxplot(df):
    x_axis_label = st.selectbox("Select x-axis data", options=other_cols, key=11)

    st.markdown("Click on the legend to (add/remove makes)")

    plot = px.box(df, x=x_axis_label, y='distance_m')
    st.plotly_chart(plot)

plot_options = ["Histogram", "Boxplot"]
continuous_cols = ["distance_m"]
other_cols = ['provider_t', 'year_move', 'move_numbe']
tab2, tab3 = st.tabs(plot_options)


with st.container():
    with st.expander('Filtering Options'):
        with st.form(key='barchart_params'):
            st.session_state.p_type = st.multiselect('Provider Type',
                                                     df.provider_t.unique(), st.session_state.p_type)
            st.session_state.year_move = st.multiselect('Year Move', df.year_move.unique(), st.session_state.year_move)
            st.session_state.dist_vals = st.slider(
                'What distances of Moves do you want to see data on?',
                0.0, float(df.distance_m.max()), (0.0, float(df.distance_m.max())))

            st.form_submit_button(label='Update Dataframe')

        filtered_df = filter_df(df, st.session_state.year_move,
                                st.session_state.p_type,
                                st.session_state.dist_vals)

        st.write(len(filtered_df))

with st.container():
    with tab2:
        histplot(filtered_df)

    with tab3:
        boxplot(filtered_df)



