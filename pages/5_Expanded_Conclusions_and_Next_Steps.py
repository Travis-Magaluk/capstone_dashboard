import streamlit as st
st.set_page_config(layout="wide")

st.title("Further Reading on Conclusions and Next Steps")

page_text = """

While this project made great strides in understanding the current landscape of dental care across the 
state of Missouri, there is still work that needs to be done to improve access to care. 
Policymakers and Lobbying groups can work on exploring the effectiveness of Expanded Licensures for Dental Hygienists 
and Mobile Dental Clinics in Underserved Areas.

#### Expanded Licensure: 

Expanding licensure for dental hygienists in rural areas is a critical initiative, particularly in Missouri where 
neighboring Kansas has already set a precedent. Our research underscores a vital point: dental hygienists are 
geographically positioned much closer to rural areas than dentists, making them the ideal healthcare providers to 
address the oral health needs of these underserved communities.

In rural areas, the scarcity of dental professionals is a pressing concern, often leading to limited access to 
essential oral healthcare services. This scarcity is exacerbated by the fact that dentists tend to concentrate in 
urban and suburban regions, leaving rural communities with disproportionately fewer options for dental care. However, 
our findings reveal that dental hygienists are more evenly distributed across the state, with a significant presence 
in rural areas. By leveraging this existing distribution, Missouri can strategically deploy dental hygienists to bridge 
the gap in oral healthcare access for rural residents.

Empowering dental hygienists with expanded licensure not only addresses the geographic disparity in dental care access 
but also maximizes the utilization of available healthcare resources. Dental hygienists possess the necessary skills 
and expertise to perform a wide range of preventative and routine dental procedures, including cleanings, fluoride 
treatments, and dental screenings. By granting them greater autonomy to practice in rural settings, Missouri can ensure 
that these essential services are readily accessible to individuals and families in need.

Furthermore, facilitating the provision of oral healthcare in rural areas has broader implications beyond individual 
health outcomes. Improved oral health contributes to overall wellbeing, enhances quality of life, and reduces 
healthcare costs associated with preventable dental conditions. Additionally, promoting dental hygiene practice in 
rural communities fosters economic development by supporting local healthcare infrastructure and promoting job creation.

As legislators and lobbyists, advocating for the expansion of dental hygienist licensure in rural areas aligns with 
our shared commitment to equitable healthcare access and the wellbeing of all Missourians. By championing this 
initiative, we have the opportunity to make tangible strides towards addressing healthcare disparities and building 
healthier, more resilient communities across the state.

#### Mobile Dental Clinics in Underserved Areas:

Mobile dental clinics are a lifeline for underserved areas where traditional dental practices may not be feasible. 
These clinics, housed in specially equipped vehicles, bring essential oral healthcare directly to communities facing 
geographical barriers or limited resources. By eliminating transportation costs and logistical challenges, mobile 
clinics ensure that individuals in remote or isolated areas can access dental care without hardship.

In addition to providing basic services like screenings and cleanings, mobile clinics focus on preventive care and 
early intervention, reducing the need for costly treatments later on. By engaging with local residents and tailoring 
services to meet specific needs, these clinics build trust and empower communities to prioritize their oral health.

In essence, mobile dental clinics serve as beacons of hope, promoting inclusivity and equity in healthcare delivery 
by bridging gaps in access and empowering underserved communities to take charge of their oral health.

#### Target Community Based Organizations (CBOs):

Community Based Organizations (CBOs) play a pivotal role in advocating for dental care in severe need areas. 
By partnering with CBOs, dental professionals can leverage existing networks and resources to reach underserved 
communities more effectively. These organizations are often deeply embedded within the communities they serve, 
possessing intimate knowledge of local needs and challenges. By collaborating with CBOs, dental care providers can 
gain valuable insights, build trust, and tailor their services to meet the specific needs of each community. 
Additionally, CBOs can help raise awareness about the importance of oral health, mobilize community members, 
and advocate for policies that promote equitable access to dental care. Together, CBOs and dental professionals 
can work towards ensuring that even the most underserved areas have access to the dental care they desperately need.

#### Future Analytics Work: 

While our project dove deep into understanding the distribution of dental providers across the state, modeling future 
need, and an exploration of the movement of providers across the state, there is still work that can be done to further 
explore this issue and provide value to key stakeholders. 

One such area for analysis would be doing a network analysis exploring the optimal placement of providers or mobile 
dental clinics to enable as many people to attend as possible. 

Further work and analysis understanding the movement of providers would be valuable to gain a deeper understanding of 
where and why providers move. Are they moving from areas of high need to low need and vice versa? In addition to 
modeling, this could involve surveys to dental providers to understand why they moved, what is the need level of that 
location, and what could be done at the state level to incentivize providers to practice in underserved areas.

"""


st.markdown(page_text)


st.sidebar.header('How to use this dashboard:')
st.sidebar.markdown("""Click through the pages in the sidebar above to view different 
                    parts of the dental provider analysis.
                    Each page focuses on answering different a question about 
                    dental providers in the state of missouri. """)