import streamlit as st
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import sqlalchemy
import geopandas as gpd
import geopandas as gpd
from shapely import wkt
from sqlalchemy.orm import Session

#
#
#This is a weird one. I am trying to use the built in connection, but get an
#error I can do it with having the credentials in the .py file
# would like to figure out how to either make this work or pull from the
# secrets .toml file using the code on github in the streamlit module.
#
#
st.title("Test Choropleth")
st.header("First Try at creating a cloropleth map in plotly and streamlit")

conn = st.connection("postgresql", type="sql")

SQL = 'SELECT * FROM mo_counties'

# Use GeoPandas to read data from PostGIS
gdf = gpd.read_postgis(SQL, conn, geom_col='geom')

# Displ ay the GeoDataFrame
st.write(gdf)
