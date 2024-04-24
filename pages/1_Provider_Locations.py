import streamlit as st

st.set_page_config(layout="wide")

st.title("Provider Locations Across Missouri")

with st.container():
    col3, col4, col5 = st.columns(spec=[0.45, .1, 0.45])

    with col3:
        st.subheader('Locating Providers and Health Resources in Missouri')
        st.write('''Understanding current dental provider locations is crucial to understanding which areas
        lack dental providers and which areas have an over abundance of providers. The definitions to the right
        define other information that can be displayed on the map.''')

    with col5:
        st.subheader('HPSA Facilities (Health Professional Shortage Area Facilities):')
        st.write('''HPSA facilities are designated healthcare facilities located in areas 
                    identified as Health Professional Shortage Areas (HPSAs). 
                    These facilities on the map are designated Dental HPSA Facilities. 
                    The designation is made by the Health Resources and Services Administration (HRSA) 
                    based on various factors, including population-to-provider ratios, socioeconomic status, 
                    and health outcomes.''')
        st.subheader('Rural Census Tract Centroids')
        st.write('''Rural census tract centroids refer to the geographical center points of rural census tracts. 
                    Census tracts are small statistical subdivisions of counties or equivalent entities used for data 
                    collection and analysis by the United States Census Bureau. Rural census tracts are those designated 
                    as having 100% of their population living in rural areas.''')

import pandas as pd
import os
import geopandas as gpd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from scipy.stats import gaussian_kde

from matplotlib.lines import Line2D


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
                  'lic_exp_da': 'exp_date', 'rural_hubd': "Distance to Nearest Rural Hub",
                  'hubdist': 'Distance to Nearest HPSA Facility', 'geometry': 'geometry'}

    f_df.rename(mapper=map_rename, inplace=True, axis=1)
    f_df['Licence Type'] = f_df['Licence Type'].replace({'DEN': 'Dentist', 'DHY': 'Hygienist'})
    f_df['exp_date'] = pd.to_datetime(f_df['exp_date'])
    f_df['Year'] = pd.DatetimeIndex(f_df['exp_date']).year.astype(str)
    return f_df


def filter_df_selections(dataframe, filter_map):
    for key in filter_map:
        dataframe = dataframe[dataframe[key].isin(filter_map[key])]
    return dataframe


def create_density_plt(_df, hue, x, fill_alpha=0.3):
    fig, ax = plt.subplots()

    # Compute mean for each group
    means = {}
    p_types = _df[hue].unique()
    for p in p_types:
        means[str(p) + '_mean'] = _df.loc[_df[hue] == p, x].mean()

    # Plot KDE plot with fill
    for p in p_types:
        subset = _df[_df[hue] == p]
        density = gaussian_kde(subset[x])
        xs = np.linspace(subset[x].min(), subset[x].max(), 100)
        color = 'blue' if p.startswith('Dentist') else 'orange'
        ax.plot(xs, density(xs), color=color, label=p)
        ax.fill_between(xs, density(xs), color=color, alpha=fill_alpha)

    # Add vertical lines for means
    for p, mean in means.items():
        ax.axvline(x=mean, color='blue' if p.startswith('Dentist') else 'orange', linestyle='--', label=p)

    ax.legend()
    ax.set_xlabel(x)
    ax.set_ylabel('Density')
    ax.set_title('Smoothed Density Plot with Fill by ' + hue)

    return fig


def create_provider_stats(df):
    grouped_df = df.groupby(['Licence Type']).agg(
        Count=('id', 'count'),  # Counting the number of rows in each group
        Avg_Distance_to_Nearest_Rural=('Distance to Nearest Rural Hub', 'mean'),
        # Calculating the average distance to nearest rural hub
        Avg_Distance_to_Nearest_HPSA_Facility=('Distance to Nearest HPSA Facility', 'mean')
        # Calculating the average distance to nearest HPSA facility
    )
    grouped_df.rename(mapper={'Avg_Distance_to_Nearest_Rural': 'Nearest Rural Average',
                              'Avg_Distance_to_Nearest_HPSA_Facility': 'Nearest HPSA Average'},
                      axis=1, inplace=True)
    # Resetting index
    grouped_df.reset_index(inplace=True)

    # Displaying the resulting DataFrame
    return grouped_df


def get_arrays(df, col_to_split, keep_col):
    unique_values = df[col_to_split].unique()
    arrays = {}

    for value in unique_values:
        arrays[value.lower()] = df[df[col_to_split] == value][keep_col].values

    return arrays

def run_ranksums_statistics(dist1, dist2):
    stats_dict = {}
    statistic, p_value = stats.ranksums(dist1, dist2)
    stats_dict['Statistic'] = statistic
    stats_dict['p_value'] = p_value

    # Interpret the results
    if p_value < 0.05:
        stats_dict[
            'Message'] = "Reject the null hypothesis: There is a significant difference between the distributions."
    else:
        stats_dict[
            'Message'] = "Fail to reject the null hypothesis: There is no significant difference between the distributions."
    return stats_dict





providers = read_file('data/all_providers/all_providers.shp')
tracts = read_file('data/tracts/tracts.shp')
hpsa = read_file('data/hpsa_facility/hpsa_facilities.shp')
rural_tract_cen = read_file('data/rural_tract_pts/rural_tract_pts.shp')

cleaned_providers = clean_providers(providers)

if 'p_type' not in st.session_state:
    st.session_state['p_type'] = cleaned_providers['Licence Type'].unique()
    st.session_state.year = cleaned_providers.Year.unique()

with st.container():
    col1, col2 = st.columns(spec=[0.4, 0.6])

    with col1:
        with st.form(key='map_params'):
            st.session_state.p_type = st.multiselect('Provider Type',
                                                     cleaned_providers['Licence Type'].unique(),
                                                     st.session_state.p_type)
            st.session_state.year = st.multiselect('Year', cleaned_providers.Year.unique(), '2024')
            rural_check = st.checkbox("Check here to see rural census tract Centroids:", value=False)
            hpsa_check = st.checkbox("Check here to see HPSA Facilities:", value=False)
            st.form_submit_button(label='Update Map')
        st.subheader('Provider Statistics:')
        filter_map = {'Licence Type': st.session_state['p_type'],
                      "Year": st.session_state['year']}
        pd.set_option('display.max_colwidth', 40)  # Set maximum column width
        # pd.set_option('display.header_wrap', True)  # Allow header text to wrap
        filtered_providers = filter_df_selections(cleaned_providers, filter_map)
        prov_stats = create_provider_stats(filtered_providers)
        prov_stats = prov_stats.round(2)
        prov_stats = prov_stats.astype(str)
        st.dataframe(prov_stats.transpose())

        st.markdown("""#### Hygienist-Dentist Disparity:
With more hygienists than dentists present statewide, there's an indication 
that hygienists could take on a more prominent role in addressing the needs of underserved populations.
#### Hygienist Proximity to Rural Areas:
Hygienists tend to be situated closer to rural 
regions compared to dentists, suggesting their pivotal role in addressing oral 
health needs in underserved abd rural communities.

#### Dentist Proximity to HPSA Facilities:

While dentists are predominantly situated closer to Health Professional 
Shortage Area (HPSA) Facilities, these locations still face significant underservice. 
This prompts the crucial question: how can dentists be incentivized to provide care in these underserved facilities""")


    with col2:
        fig, ax = plt.subplots(figsize=(10, 8))
        tracts.plot(ax=ax, legend=True, color='lightgrey')
        for license_type, color in zip(['Dentist', 'Hygienist'], ['red', 'blue']):  # Specify your license types here
            subset = filtered_providers[filtered_providers['Licence Type'] == license_type]
            if not subset.empty:
                subset.plot(ax=ax, color=color, markersize=3, label=license_type, alpha=0.4)

        # Plot HPSA facilities if checked
        if hpsa_check:
            hpsa.plot(ax=ax, color='black', marker='s',  markersize=10)
            hpsa_legend = Line2D([0], [0], marker='s', color='w',
                                 markerfacecolor='black', markersize=7, label='HPSA Facilities')
        if rural_check:
            rural_tract_cen.plot(ax=ax, color='green', marker='*', markersize=10)
            rural_legend = Line2D([0], [0], marker='*', color='w',
                                  markerfacecolor='green', markersize=10, label='Rural Tract Centroids')
        ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False)
        ax.set_xticks([])  # Remove x-axis tick marks
        ax.set_yticks([])  # Remove y-axis tick marks
        handles, labels = ax.get_legend_handles_labels()
        if hpsa_check:
            handles.append(hpsa_legend)
            labels.append('HPSA Facilities')
        if rural_check:
            handles.append(rural_legend)
            labels.append('Rural Tract Centroids')
        ax.legend(handles, labels, loc='upper right')
        st.pyplot(fig)

        st.subheader('Key Insights')
        st.write('''Attention is drawn to the stark shortage of healthcare providers across the northern 
        and southeastern regions of the state. These areas face significant challenges in accessing 
        essential medical services, including dental care. The scarcity of providers underscores the 
        urgent need for targeted interventions to address healthcare disparities and ensure equitable 
        access to quality care for all residents.''')

with st.container():
    col1, col2 = st.columns(spec=[0.5, 0.5])

    with col1:
        fig1 = create_density_plt(filtered_providers, 'Licence Type', 'Distance to Nearest Rural Hub', fill_alpha=0.3)
        st.pyplot(fig1)
        try:
            array_dict = get_arrays(filtered_providers, 'Licence Type', 'Distance to Nearest Rural Hub')
            keys = list(array_dict.keys())[:2]
            stats_dict_1 = run_ranksums_statistics(array_dict[keys[0]], array_dict[keys[1]])
            st.write(stats_dict_1)
        except IndexError:
            pass
    with col2:
        fig2 = create_density_plt(filtered_providers, 'Licence Type', 'Distance to Nearest HPSA Facility', fill_alpha=0.3)
        st.pyplot(fig2)
        array_dict = get_arrays(filtered_providers, 'Licence Type', 'Distance to Nearest HPSA Facility')
        keys = list(array_dict.keys())[:2]
        stats_dict_2 = run_ranksums_statistics(array_dict[keys[0]], array_dict[keys[1]])
        st.write(stats_dict_2)

st.sidebar.header("Navigation:")
st.sidebar.markdown("""Explore the geographic distribution of dental care providers, 
including dentists and hygienists, alongside crucial demographic data, 
such as rural census tracts and Health Professional Shortage Area (HPSA) Facilities. 
Interact with the filters to customize your view, selecting specific provider types and years. 
Once you've refined your data selection, simply click "Update Map" to 
regenerate the map with your chosen parameters.""")