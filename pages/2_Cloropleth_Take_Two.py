import streamlit as st
import pandas as pd
import sqlalchemy
import geopandas as gpd
import psycopg2

import plotly.express as px

st.set_page_config(layout="wide")

st.title("Test Choropleth")
st.header("First Try at creating a cloropleth map in plotly and streamlit")

connection = psycopg2.connect(database = st.session_state.database,
                              user = st.session_state.user,
                              host = 'capstone.c94ookq24fln.us-east-2.rds.amazonaws.com',
                              password = st.session_state['database_password'])


SQL = "SELECT * FROM mo_counties;"

mo_counties = gpd.read_postgis(SQL,connection)
fig = px.choropleth(mo_counties,
                   geojson=mo_counties.geom,
                   locations=mo_counties.index,
                   projection="mercator")
fig.update_layout(
    autosize=False,
    width=800,
    height=800,
)
fig.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig, use_container_width=True)