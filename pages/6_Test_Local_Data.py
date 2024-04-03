import streamlit as st
import pandas as pd
import os
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

@st.cache_data
def read_file(filepath):
    df = gpd.read_file(filepath, encoding='utf-8')
    return df
def clean_providers(df):
    cols_keep = ['id', 'ba_city', 'ba_state', 'ba_cnty', 'lic_profes', 'lic_number',
                 'lic_exp_da', 'rural_hubd', 'hubdist', 'geometry']
    f_df = df.filter(items=cols_keep, axis=1)
    map_rename = {'id': 'id', 'ba_city': 'City', 'ba_state': 'State', 'ba_cnty': 'County',
                  'lic_profes': "Licence Type", 'lic_number': 'Licence Number',
                 'lic_exp_da':'exp_date', 'rural_hubd': "Distance to Nearest Rural Hub",
                  'hubdist': 'Distance to Nearest HPSA Facility', 'geometry': 'geometry'}

    f_df.rename(mapper = map_rename,inplace=True, axis=1)
    f_df['exp_date'] = pd.to_datetime(f_df['exp_date'])
    f_df['Year'] = pd.DatetimeIndex(f_df['exp_date']).year.astype(str)
    return f_df

def filter_df_selections(dataframe, filter_map):
    for key in filter_map:
        dataframe = dataframe[dataframe[key].isin(filter_map[key])]
    return dataframe

providers = read_file('data/all_providers/all_providers.shp')
tracts = read_file('data/tracts/tracts.shp')
hpsa = read_file('data/hpsa_facility/hpsa_facilities.shp')
rural_tract_cen = read_file('data/rural_tract_pts/rural_tract_pts.shp')

cleaned_providers = clean_providers(providers)


if 'p_type' not in st.session_state:
    st.session_state['p_type'] = cleaned_providers['Licence Type'].unique()
    st.session_state.year = cleaned_providers.Year.unique()

with st.container():
    col1, col2 = st.columns(spec=[0.3, 0.7])

    with col1:
       with st.form(key='map_params'):
        st.session_state.p_type = st.multiselect('Provider Type',
                                                 cleaned_providers['Licence Type'].unique(), st.session_state.p_type)
        st.session_state.year = st.multiselect('Year', cleaned_providers.Year.unique(), st.session_state.year)
        st.form_submit_button(label='Update Dataframe')

    filter_map = {'Licence Type': st.session_state['p_type'],
                      "Year": st.session_state['year']}
    filtered_providers = filter_df_selections(cleaned_providers, filter_map)



    with col2:
        fig, ax = plt.subplots(figsize=(10, 8))
        tracts.plot(ax=ax, legend=True)
        filtered_providers.plot(ax=ax, color='red', markersize=3, label='Dental Providers', alpha=1)
        hpsa.plot(ax=ax, color='black', markersize=5)
        rural_tract_cen.plot(ax=ax, color='pink', markersize=10)
        ax.set_title('Census Tract Provider Counts')
        st.pyplot(fig)



