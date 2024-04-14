import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import plotly.express as px
import json

st.title("Census Tracts by Need Level")
st.header("Explore the need in 2022 vs. Projected Need in 2030.")


@st.cache_data
def read_file(filepath):
    df = gpd.read_file(filepath, encoding='utf-8')
    return df


@st.cache_data
def convert(_df):
    json_data = _df.to_json()
    return json_data


def process_dataframe(df):
    category_mapping = {
        'no need': 1,
        'low': 2,
        'moderate': 3,
        'high': 4,
        'severe': 5
    }
    cols_to_keep = ['geoid', 'namelsad', 'need2022', 'need2030_n', 'mo_countie', 'geometry']

    df = df[cols_to_keep]
    df['geoid'] = df['geoid'].astype(str)
    df['need_category_2022'] = df['need2022'].map(category_mapping)
    df['need_category_2030'] = df['need2030_n'].map(category_mapping)

    return df

@st.cache_resource
def generate_map(need_year, fill_opacity, tooltip):
    center_lat, center_lon = need['geometry'].centroid.y.mean(), need['geometry'].centroid.x.mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

    folium.Choropleth(
        geo_data=geojson_data,
        name='choropleth',
        data=need,
        columns=['geoid', need_year],
        key_on='feature.properties.geoid',
        fill_color='Reds',
        fill_opacity=fill_opacity,
        line_opacity=.3,
        line_color='black',  # specify line color
        line_weight=.5,
        legend_name='Legend',
        categorical=True,
    ).add_to(m)
    if tooltip:
        folium.GeoJson(
            geojson_data,
            name="geojson",
            tooltip=folium.features.GeoJsonTooltip(
                fields=['geoid', need_year],  # include additional fields for tooltip
                aliases=['Geoid', 'Need Level'],  # aliases for field names
                labels=True,  # display field names as labels
            )
        ).add_to(m)
    return m


need = read_file('data/need/need.shp')

need = process_dataframe(need)
geojson_data = convert(need)
with st.container():
    col1, col2 = st.columns(spec=[0.3, 0.7])

    with col1:
        with st.form(key='map_params'):
            need_year = st.radio(label='Select the year you want to view:',
                                 options=['2022', '2030'])
            tooltip = st.checkbox("Check here for tooltip:", value=False)
            st.form_submit_button(label='Update Map')

        st.write(need_year)
        st.write(tooltip)

    with col2:
        if need_year == '2022':
            m = generate_map('need_category_2022', 0.7, tooltip)
            folium_static(m)

        else:
            m = generate_map('need_category_2030', 0.7, tooltip)
            folium_static(m)
