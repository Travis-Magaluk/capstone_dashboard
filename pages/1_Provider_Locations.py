import streamlit as st
import pandas as pd
import os
import geopandas as gpd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
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
                  'lic_exp_da': 'exp_date', 'rural_hubd': "Distance to Nearest Rural Hub",
                  'hubdist': 'Distance to Nearest HPSA Facility', 'geometry': 'geometry'}

    f_df.rename(mapper=map_rename, inplace=True, axis=1)
    f_df['exp_date'] = pd.to_datetime(f_df['exp_date'])
    f_df['Year'] = pd.DatetimeIndex(f_df['exp_date']).year.astype(str)
    return f_df


def filter_df_selections(dataframe, filter_map):
    for key in filter_map:
        dataframe = dataframe[dataframe[key].isin(filter_map[key])]
    return dataframe


@st.cache_data
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
        ax.plot(xs, density(xs), label=p)
        ax.fill_between(xs, density(xs), alpha=fill_alpha)

    # Add vertical lines for means
    for p, mean in means.items():
        ax.axvline(x=mean, color='blue' if p.startswith('DEN') else 'orange', linestyle='--', label=p)

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


st.title("Provider Locations Across Missouri")
st.header("Map showing provider locations in the state of missouri "
          "Explore the data and see where providers are located. "
          "Also see where Rural Areas are (100% rural population)."
          "and see where Health Professional Shortage areas are located too.")

with st.container():
    col1, col2 = st.columns(spec=[0.4, 0.6])

    with col1:
        with st.form(key='map_params'):
            st.session_state.p_type = st.multiselect('Provider Type',
                                                     cleaned_providers['Licence Type'].unique(),
                                                     st.session_state.p_type)
            st.session_state.year = st.multiselect('Year', cleaned_providers.Year.unique(), st.session_state.year)
            rural_check = st.checkbox("Check here to see rural census tract Centroids:", value=False)
            hpsa_check = st.checkbox("Check here to see HPSA Facilities:", value=False)
            st.form_submit_button(label='Update Dataframe')
        st.subheader('Basic Stats:')
        filter_map = {'Licence Type': st.session_state['p_type'],
                      "Year": st.session_state['year']}
        pd.set_option('display.max_colwidth', 40)  # Set maximum column width
        # pd.set_option('display.header_wrap', True)  # Allow header text to wrap
        filtered_providers = filter_df_selections(cleaned_providers, filter_map)
        prov_stats = create_provider_stats(filtered_providers)
        st.dataframe(prov_stats.transpose())


    with col2:
        fig, ax = plt.subplots(figsize=(10, 8))
        tracts.plot(ax=ax, legend=True, color='lightblue')
        for license_type, color in zip(['DEN', 'DHY'], ['red', 'blue']):  # Specify your license types here
            subset = filtered_providers[filtered_providers['Licence Type'] == license_type]
            if not subset.empty:
                subset.plot(ax=ax, color=color, markersize=3, label=license_type, alpha=0.4)
        # Plot HPSA facilities if checked
        if hpsa_check:
            hpsa.plot(ax=ax, color='green', markersize=5)
        if rural_check:
            rural_tract_cen.plot(ax=ax, color='pink', markersize=10)
        ax.set_title('Census Tract Provider Counts')
        st.pyplot(fig)

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

