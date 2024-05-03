import streamlit as st

st.set_page_config(layout="wide")

st.title('Geospatial Analysis')

opening_text = """
#### Geospatial Analysis Overview and Terms

Our geospatial analyses aimed to identify and analyze significant clusters where dental services are lacking. 
We operationalized our "need" outcome in 2 different ways:
- Population-based
- Distance-based

We identified significant need clusters using Moran's I. It measures the overall spatial similarity of regions. 
Values range from -1 to 1 (-1 perfect dispersion, 0 perfect randomness, and +1 perfect clustering of similar values). 

Next, we utilized Ordinary Least Squares Regression to identify the Census indicators most related to each dependent 
variable. 

Finally, we conducted Geographically Weighted Regression (GWR) and Multiscale Geographically Weighted Regression (MGWR)
to investigate geospatial variation in our predictor variables. 
While GWR tests for the global fit of predictors at a uniform scale (Golden section bandwidth), 
MGWR tests for the local fit of Census predictors at a variable scale (optimized number of nearest neighbors). 
"""

st.markdown(opening_text)

tab1, tab2, tab3 = st.tabs(["Missouri - Providers per 4k", "Missouri - Distance Based", "Kansas City"])

with tab1:
    st.markdown('''
    ### Dentists per Four-Thousand Census Tract Population
    
    Our first dependent variable was population-based, the density of dentists per 4K tract population. 
    The 1:4000 ratio is the Health Professional Shortage Area (HPSA) standard for estimating provider need. 
    The number of dentists per 4K people ranged between 0 and 95 for the 1655 Missouri Census tracts. While the average 
    per tract was 2, only 317 tracts met the HPSA threshold. There were 689 Census tracts with no dentist at all.''')
    col1, col2 = st.columns(spec=[0.5, 0.5])
    with col1:
        st.subheader('Moran\'s I for 4k Tract Population')
        st.image('images/GeoAnalysis/tab1_img1.png')
        st.markdown("""
        #### Takeaways
        
        The map above shows significant clusters for dentist density per 4K tract population 
        (Moran’s I = 0.696, p < .001). 
        
        - The light green area represents a large cluster of low dentist density.
        - The dark red regions show zones where dentists are concentrated.
        
        """)
    with col2:
        st.subheader('Predictive Power of 4 Variables')
        st.image('images/GeoAnalysis/tab1_img2.png')

        st.markdown("""
        #### Takeaways
        
        Using ordinary least squares regression, we were able to significantly predict 14% of the variance in dentist 
        density using the following 4 Census predictors: 
        - Median monthly household costs (6%)
        - Percent of the population commuting greater than 44 minutes to work or shopping (4%)
        - Percent of the population commuting greater than 20 minutes to work or shopping (2%)
        - Percent of tract population using SNAP benefits (2%). 
        
        While the **bright yellow areas** of the map represent where these 4 predictors **best describe** 
        the tract population, the **dark blue areas** are those where the predictors **do not describe** the tract 
        population as well.
        
        14% of variance accounted for is a low number. We decided to try another variable to see if we could 
        account for more of the variance. Head to the next tab to see the distance based results.
        """)
with tab2:
    with st.container():

        st.markdown("""
        ### Distance Based Dependent Variable
        
        Our second dependent variable was distance-based: **the straight-line distance between each tract centroid 
        point and the nearest dentist.** 
        
        The distance to the nearest dentist ranged from 0.014 miles to 26.03 miles, 
        with an average distance of 1.99 miles. 
        
        We calculated a value for each of the 1655 Missouri tract points.
        """)
        col1, col2 = st.columns(spec=[0.5, 0.5])
        with col1:
            st.subheader('Moran\'s I for Distance Based Measures')
            st.image('images/GeoAnalysis/tab2_img1.png')
            st.markdown("""
            #### Results
            
            The first map shows significant clusters for distance to the nearest dentist 
            (Moran’s I = 0.861, p < .001). While the **dark red** area represents a **large cluster of high 
            commute distances** to the nearest dentist, the **light green** regions near bigger cities show zones 
            where prospective dental patients do not have to travel as far for care.
            """)
        with col2:
            st.subheader('Predictive Power of 4 Variables')
            st.image('images/GeoAnalysis/tab2_img2.png')
            st.markdown("""
            #### Results and Takeaways
            Using ordinary least squares regression, we were able to significantly predict 69% of the variance in the 
            distance to the nearest dentist using the following 6 Census predictors: 
            - Rural-urban commuting area (23%) 
            - Percent of population commuting greater than 40 miles to work or shopping (19%)
            - Median monthly household costs (16%)
            - Total number of households (6%)
            - Percent of population uninsured (3%)
            - 12-month median income (2%)
            
            While the **bright yellow areas** of the map represent where these 6 predictors **best describe** the tract 
            population, the **dark blue areas** are those where the predictors **do not describe** the tract population 
            as well.
            """)
    with st.container():
        col3, col4 = st.columns(spec=[0.5, 0.5])
        with col3:
            st.subheader('How Do the Predictors Cluster')
            st.image('images/GeoAnalysis/tab2_img3.png')
            st.markdown("""
            This map shows significant clusters of household cost of living (Moran’s I = 0.907, p < .001). 
            While the **light green area** is a large cluster showing **lower monthly household costs**, 
            the **dark red areas** are those with a **higher cost of living**.
            """)
        with col4:
            st.subheader('Global predictive value of median monthly household costs: Golden section bandwidth')
            st.image('images/GeoAnalysis/tab2_img4.png')
            st.markdown("""
                        The above Geographically Weighted Regression (GWR) map shows areas where a particular predictor 
                        best describes the tract population using a uniform bandwidth (the same number of nearest 
                        neighbors for all variables). GWR shows that our predictors explain about 44% of the variance 
                        in the distance to the nearest dentist when geospatial relationships are taken into account.
                        
                        **What is the difference between the blue and grey. We should highlight for our audience** 
                        """)
    with st.container():
        col5, col6 = st.columns(spec=[0.5, 0.5])
        with col5:
            st.subheader('Local predictive value of median monthly household costs: Variable bandwidth by predictor')
            st.image('images/GeoAnalysis/tab2_img5.png')
            st.markdown("""
            The Multiscale Geographically Weighted Regression (MGWR) map shows areas where a particular predictor best 
            describes the tract population using a variable bandwidth (optimizing the number of nearest neighbors to 
            understand differential spatial effects for our predictors). MGWR shows that our predictors explain almost 
            60% of the variance in the distance to the nearest dentist when geospatial relationships are considered. 
            
            **What is the difference between the blue and grey. We should highlight for our audience**
            """)
        with col6:
            st.subheader('I think we should have a big picture so what for our stakeholders here! Or at the bottom')
with tab3:
    st.image('images/img3.png')

