import streamlit as st
import pandas as pd
import sqlalchemy
import geopandas as gpd
import psycopg2
import matplotlib.pyplot as plt
import plotly.express as px

conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM credentials;', ttl="10m")

st.title("Choropleth Map")
st.header("Working on displaying different data through a Choropleth Map")

connection = psycopg2.connect(database='dentdb',
                              user=df.iloc[0][3],
                              host=df.iloc[0][1],
                              password=df.iloc[0][4])

SQL = "SELECT * FROM travis_testing;"
SQL2 = "SELECT * FROM all_providers_dist"
moves = gpd.read_postgis(SQL2, connection)
mo_counties = gpd.read_postgis(SQL, connection)
st.write(len(moves))
mo_counties['dhyg_cnt_trct_year_hyg_count'] = mo_counties['dhyg_cnt_trct_year_hyg_count'].fillna(0)
moves = moves[moves['lic_exp_da'] == '11/30/2022']
moves = moves[moves['lic_profes'] == 'DEN']
st.write(len(moves))
st.header('Census Tract Population Choropleth Map')
fig, ax = plt.subplots(figsize=(10, 8))
mo_counties.plot(column='dhyg_cnt_trct_year_hyg_count', cmap='Blues', ax=ax, legend=True)
moves.plot(ax=ax, color='red', markersize=3, label='Dental Providers', alpha=0.2)
ax.set_title('Census Tract Provider Counts')
st.pyplot(fig)
