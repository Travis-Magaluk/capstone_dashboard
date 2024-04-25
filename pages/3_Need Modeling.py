import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import plotly.express as px
import json

st.set_page_config(layout="wide")
st.title("Census Tracts by Need Level")
st.subheader("The images below showcase current dental provider need in 2022, "
             "future predicted need in 2030, or the change in need from 2022 to 2030. "
             "Need is scaled from 1, being no need, to 5, being severe need."
             "In the change of need, negative values indicate that there is a decreasing need, "
             "whereas positive numbers indicate an increasing need from 2022 to 2030.")

st.sidebar.header("Navigation:")
st.sidebar.markdown("""Zoom in and out of the map with you mouse to see the need level for dental providers
in various census tracts. Click and drag the map to pan. \n 
Toggle between actual need in 2022, predicted need in 2030, or see the 'Change' in 
need from 2022 to 2030. \n 
Click the tooltip checkbox to see hover over information for each census tract. \n
Click the 'X' in the navigation bar top right to make more room to explore the visualizations. """)

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
    cols_to_keep = ['geoid', 'namelsad', 'need2022', 'need2030_n',
                    'mo_countie', 'geometry', 'minority_M', 'minority_1']

    df = df[cols_to_keep]
    df['geoid'] = df['geoid'].astype(str)
    df['need_category_2022'] = df['need2022'].map(category_mapping)
    df['need_category_2030'] = df['need2030_n'].map(category_mapping)
    df['need_change'] = df['need_category_2030'] - df['need_category_2022']

    return df


@st.cache_resource
def generate_map(need_year, fill_opacity, tooltip):
    center_lat, center_lon = need['geometry'].centroid.y.mean(), need['geometry'].centroid.x.mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=7)
    color = "Spectral" if need_year == 'Change' else 'Reds'
    folium.Choropleth(
        geo_data=geojson_data,
        name='choropleth',
        data=need,
        columns=['geoid', need_year],
        key_on='feature.properties.geoid',
        fill_color=color,
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
                fields=['geoid', 'namelsad', 'mo_countie',
                        'need2022', 'need2030_n', 'minority_M'],  # include additional fields for tooltip
                aliases=['Geoid', 'Census Tract',
                         'County', '2022 Need Level', "2030 Need Level",
                         'Percent Minority'],  # aliases for field namess

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
                                 options=['2022', '2030', 'Change'])
            tooltip = st.checkbox("Check here for tooltip:", value=True)
            st.form_submit_button(label='Update Map')

            st.subheader("Key")
            if need_year == '2022' or need_year == '2030':
                st.write('Lighter areas indicate no to low need. Darker areas indicate high to severe need.')
            else:
                st.write("""Lighter areas mean that the need is Decreasing.
                        Darker Areas mean that the need is increasing.""")

    with col2:
        if need_year == '2022':
            m = generate_map('need_category_2022', 0.7, tooltip)
            folium_static(m)

        elif need_year == '2030':
            m = generate_map('need_category_2030', 0.7, tooltip)
            folium_static(m)
        else:
            m = generate_map('need_change', 0.7, tooltip)
            folium_static(m)

st.subheader('Key Findings')
st.write('It was found that many severe census tracts tend to be concentrated in '
         'majority racial minority census tracts. Hovering over each census tract will '
         'provide detail on the % minority illustrating this finding. ')

