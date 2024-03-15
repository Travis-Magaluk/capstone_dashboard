import streamlit as st
import pandas as pd
import sqlalchemy
import geopandas as gpd
import psycopg2

import plotly.express as px
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM credentials;', ttl="10m")

st.title("Choropleth Map")
st.header("Working on displaying different data through a Choropleth Map")

connection = psycopg2.connect(database = 'dentdb',
                              user = df.iloc[0][3],
                              host = df.iloc[0][1],
                              password = df.iloc[0][4])


SQL = "SELECT * FROM travis_testing;"

mo_counties = gpd.read_postgis(SQL,connection)

mo_counties['dhyg_cnt_trct_year_hyg_count'] = mo_counties['dhyg_cnt_trct_year_hyg_count'].fillna(0)

fig = px.choropleth(mo_counties,
                   geojson=mo_counties.geom,
                   locations=mo_counties.index,
                   projection="mercator",
                    color='dhyg_cnt_trct_year_hyg_count',
                    labels={'dhyg_cnt_trct_year_hyg_count':'Hygienists in 2020'})
fig.update_layout(
    autosize=False,
    width=800,
    height=800,
)
fig.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig, use_container_width=True)

df = px.data.carshare()
fig = px.scatter_mapbox(df, lat="centroid_lat", lon="centroid_lon", color="peak_hour", size="car_hours",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
                  mapbox_style="carto-positron")
st.plotly_chart(fig)