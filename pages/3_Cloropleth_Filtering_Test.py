import streamlit as st
import pandas as pd
import sqlalchemy
import geopandas as gpd
import psycopg2

import plotly.express as px
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM credentials;', ttl="10m")

st.title("Missouri Census Tract Features")
st.header("This map will display various features for census tracts across the state of Missouri for the year 2022")

connection = psycopg2.connect(database = 'dentdb',
                              user = df.username[0],
                              host = df.host[0],
                              password = df.password[0])


SQL = "SELECT * FROM spat_autocorr_layer_3;"


mo_counties = gpd.read_postgis(SQL,connection)

with st.form(key='cloropleth_filter'):
    col_selection = st.radio('Fill Values',
                             options=['tot_pop', 'pop_ins', 'pop_unis', 'pct_unins',
                                      'dent_4k', 'need2022', 'need2030'])

    st.form_submit_button(label='Update Dataframe')

fig = px.choropleth(mo_counties,
                   geojson=mo_counties.geom,
                   locations=mo_counties.index,
                   projection="mercator",
                    color=col_selection,
                    labels={col_selection:col_selection},
                    title=f'{str.capitalize(col_selection)} by Census Tracts for Year of 2022')
fig.update_layout(
    autosize=False,
    width=800,
    height=800,
)
fig.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig, use_container_width=True)
