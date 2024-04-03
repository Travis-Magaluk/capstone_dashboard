def secrets(self) -> AttrDict:
    """Get the secrets for this connection from the corresponding st.secrets section.

    We expect this property to be used primarily by connection authors when they
    are implementing their class' ``_connect`` method. User scripts should, for the
    most part, have no reason to use this property.
    """
    connections_section = None
    if secrets_singleton.load_if_toml_exists():
        connections_section = secrets_singleton.get("connections")

    if type(connections_section) is not AttrDict:
        return AttrDict({})

    return connections_section.get(self._connection_name, AttrDict({}))


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
