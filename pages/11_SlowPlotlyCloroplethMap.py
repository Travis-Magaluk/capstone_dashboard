import streamlit as st
import pandas as pd
import geopandas as gpd

import plotly.express as px

st.title("Missouri Census Tract Features")
st.header("This map will display various features for census tracts across the state of Missouri for the year 2022")


@st.cache_data
def read_file(filepath):
    df = gpd.read_file(filepath, encoding='utf-8')
    return df


@st.cache_data
def create_choropleth_plot(_df, need_year):
    fig = px.choropleth(_df,
                        geojson=_df.geometry,
                        locations=_df.index,
                        projection="mercator",
                        color=need_year,
                        hover_data=[need_year, 'mo_countie', 'namelsad'],
                        title=need_year)
    fig.update_layout(
        autosize=False,
        width=800,
        height=800, )
    fig.update_geos(fitbounds="locations", visible=False)
    return fig


need = read_file('data/need/need.shp')


with st.form(key='cloropleth_filter'):
    col_selection = st.radio('Fill Values',
                             options=['need2022', 'need2030_n'])

    st.form_submit_button(label='Update Dataframe')

fig = create_choropleth_plot(need, col_selection)

st.plotly_chart(fig, use_container_width=True)
