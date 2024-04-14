import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import plotly.express as px
import json

st.title("Missouri Census Tract Features")
st.header("This map will display various features for census tracts across the state of Missouri for the year 2022")


@st.cache_data
def read_file(filepath):
    df = gpd.read_file(filepath, encoding='utf-8')
    return df


need = read_file('data/need/need.shp')
need['geoid'] = need['geoid'].astype(str)

category_mapping = {
    'no need': 1,
    'low': 2,
    'moderate': 3,
    'high': 4,
    'severe': 5
}
color_mapping = {
    1: '#0000FF',
    2: '#4B0082',
    3: '#8B00FF',
    4: '#C20088',
    5: '#FF0000'
}

# Map the categorical values to numerical values
need['numeric_category'] = need['need2022'].map(category_mapping)

geojson_data = need.to_json()

# Create a Folium map centered around the first geometry
center_lat, center_lon = need['geometry'].centroid.y.mean(), need['geometry'].centroid.x.mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

myStyle = {
    "weight": 5,
    "opacity": 0.0
}

folium.Choropleth(
    geo_data=geojson_data,
    name='choropleth',
    data=need,
    columns=['geoid', 'numeric_category'],
    key_on='feature.properties.geoid',
    fill_color=None,
    fill_opacity=0.7,
    line_opacity=1,
    line_color='black',  # specify line color
    line_weight=1,
    legend_name='Legend',
    categorical=True,
    style_function=lambda x: {
        'fillColor': color_mapping.get(x['properties']['numeric_category'], '#FFFFFF'),  # map need levels to colors
        'color': 'black',  # specify line color
        'weight': 1,  # specify line weight
        'fillOpacity': 0.7  # specify fill opacity
    }
).add_to(m)
# Add GeoJSON data to the map
folium.GeoJson(
    geojson_data,
    name="geojson",
    tooltip=folium.features.GeoJsonTooltip(
        fields=['geoid', 'name', 'need2022'],  # include 'need2022' field for tooltip
        aliases=['Geoid', 'Name', 'Need Level'],  # aliases for field names
        labels=True,  # display field names as labels
    )
).add_to(m)

folium_static(m)
