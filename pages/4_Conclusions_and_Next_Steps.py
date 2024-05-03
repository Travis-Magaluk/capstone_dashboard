import streamlit as st
st.set_page_config(layout="wide")

st.title("Conclusions and Next Steps")


key_findings = """

Areas with **high** minority populations are predicted to be **more likely** to have severe dental need. 
Controlling for differences in population does not relieve this concern. 

Dental hygienists locate significantly closer to rural areas than dentists do. 

Further drive times are correlated with:
- Low median income
- Low insurance rates
- Rural areas
- Long commutes to work/shopping

Shorter drive times are correlated with:
- High monthly income
- Household density

#### Why does this matter? 

Through this project, the group has been able to identify where dental providers are located across Missouri, 
predict future need in census tracts, and describe the population in low and high provider density areas.

This information will serve to educate dental service organizations, dental schools, current dental health providers, 
and policymakers on existing needs across the state. 

The ultimate goal of this research is to help Missourians - by providing information to make informed, 
data-driven decisions surrounding future dental care. 


"""


next_steps = """

#### Expanded Licensure
- Expanding licensure for dental hygienists in rural areas is a critical initiative for Missouri, 
where neighboring Kansas has already set a precedent. 
- Our research underscores a vital point: dental hygienists are geographically positioned much closer to 
rural areas than dentists, making them the ideal healthcare providers to address the oral 
health needs of these underserved communities. 

#### Mobile Dental Clinics in Underserved Areas
- Mobile dental clinics are a lifeline for underserved areas where traditional dental practices may not be feasible. 
- These clinics, housed in specially equipped vehicles, bring essential oral healthcare directly to 
communities facing geographical barriers or limited resources.

#### Target Community Based Organizations (CBOs)
- Community Based Organizations (CBOs) play a pivotal role in advocating for dental care in severe need areas.
- By partnering with CBOs, dental professionals can leverage existing networks and 
resources to reach underserved communities more effectively. 

#### Future Analytics Work
- There is still work that can be done to further explore this issue and provide value to key stakeholders
- Some ways to pursue this work:
    - Network analysis for optimal provider or clinic placement
    - Providing surveys to providers to gain insights into why and where they moved their practice 
    - Conducting economic impact assessments and sustainability of mobile dental clinics in underserved areas
    - Exploring technological innovations to enhance access to dental care in remote communities
    - Collaborating with public health agencies to integrate oral healthcare into broader health initiatives
    - Evaluating the potential impact of policy changes on dental care access and outcomes
    - Engaging with community stakeholders to gather qualitative insights and perspectives on oral health needs
    - Developing data-driven strategies for addressing disparities in dental care access and outcomes

"""
st.header('Key Findings')
st.markdown(key_findings)

st.header("Next Steps")
st.markdown(next_steps)
st.sidebar.header('How to use this dashboard:')
st.sidebar.markdown("""Click through the pages in the sidebar above to view different 
                    parts of the dental provider analysis.
                    Each page focuses on answering different a question about 
                    dental providers in the state of missouri. """)