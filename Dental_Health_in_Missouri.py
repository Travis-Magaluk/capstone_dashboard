import streamlit as st
st.set_page_config(layout="wide")

st.title("Access to Dental Care")
st.header('An Exploration of Dental Care in Missouri')
st.markdown("#")

overview = """
Our dashboard presents an analysis spanning from 2010 to 2024, focusing on provider data of dentists 
and dental hygienists in Missouri. Through meticulous examination, we've outlined their 
geographical distribution and their proximity to rural areas.

This culmination of analytical work aims to facilitate future 
decision-making processes and furnish stakeholders with crucial insights.

Across Missouri, access to dental care faces significant challenges due to provider shortages 
dispersed throughout the state. These shortages have profound implications, leading to 
prevalent issues such as cavities, periodontal diseases, and their consequential impacts on 
systemic health, including diabetes, heart disease, and oral cancer.

With this dashboard, we strive to provide a clear understanding of these barriers, 
highlighting the importance of addressing provider shortages for 
better healthcare access and improved public health outcomes.

"""



problem = """
##### Unveiling the Dental Health Crisis in Missouri

In the heart of the United States lies Missouri, a state grappling with a silent epidemic: 
poor dental health. Behind the serene landscapes and bustling cities lies a stark reality, 
where access to quality dental care remains a persistent challenge for many residents.

##### Statistics Speak Louder than Words

- According to the Missouri Department of Health and Senior Services, approximately 45% of 
Missourians lack dental insurance, one of the highest uninsured rates in the nation.

- The shortage of dental providers in Missouri disproportionately affects rural areas, 
where over 40% of the state’s population resides. Access to dental care is limited. 

- Alarmingly, over 25% of Missouri's adults report that they have not visited a
 dentist within the past year, citing cost as the primary barrier.

##### The Hidden Costs of Neglected Oral Health

The repercussions of poor dental health extend far beyond mere discomfort. 
Untreated cavities, gum disease, and oral infections can lead to health issues such as 
diabetes, heart disease, and even oral cancer.

##### Voices from the Heartland

> ***"Forty-two percent of our patients are driving from outside the Columbia area to get work done, 
> because they don't have the dental care that they need provided in the smaller cities 
> that they are from," Parrott, who owns Aspen Dental in Columbia and Jefferson City***

> ***"Taking the time off of work to have to drive further away because we don't 
> have enough dentists in the area to accommodate everyone's needs," Vandelicht, Missouri Resident***

##### Shedding Light on the Path Forward

Amidst these challenges, there is hope. By acknowledging the gravity of the situation and working collaboratively, 
we can pave the way for meaningful change. Through targeted interventions, policy advocacy, 
and community engagement, we can strive towards a future where every Missourian has access to 
the dental care they need and deserve.
"""

intended_audience = """
##### Corporate Dentistry
For Dental Service Organizations (Corporate Dentistry), this platform offers valuable insights into 
areas of both need and opportunity for establishing practices and engaging providers. 
Executives can leverage this data to strategize expansion plans and target underserved regions effectively.

##### Dental Schools
Dental Schools benefit from access to educational materials tailored to their curriculum, 
providing students and faculty with crucial information on areas where providers are most needed. 
This empowers future dental professionals with insights that align with community health needs, 
fostering a sense of responsibility to work with underserved populations.

##### Current Dental Health Providers
Current Dental Health Providers are encouraged to consider providing care in rural and high-need areas. 
Our dashboard acts as a catalyst for change, motivating providers to explore opportunities where their services 
are most urgently required, thus bridging gaps in access to dental care.

##### Policymakers
Policymakers find support for informed decision-making regarding expanded licensure for dental hygienists 
and incentives for providers to practice in underserved regions. Our data-driven approach equips policymakers 
with evidence-based arguments to advocate for policies that address workforce shortages and promote 
equitable access to dental care across communities.

"""

with st.container():
    col1, col2, col3 = st.columns(spec=[0.45, 0.1, 0.45])

    with col1:
        st.subheader("Dashboard Overview")
        st.markdown(overview)

        st.subheader('Intended Audience')
        st.markdown(intended_audience)
    with col2:
       st.header('')

    with col3:
       st.subheader("The Problem")
       st.markdown(problem)

    st.write("\n\n\n")


st.sidebar.header('How to use this dashboard:')
st.sidebar.markdown("""Click through the pages in the sidebar above to view different 
                    parts of the dental provider analysis.
                    Each page focuses on answering different a question about 
                    dental providers in the state of missouri. """)