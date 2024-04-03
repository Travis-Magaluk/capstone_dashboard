import streamlit as st
st.set_page_config(layout="wide")

st.title("Rural Access to Dental Services")
st.markdown("#")




problem = """
Many people in missouri are lacking adequate access to dental care. This is what some people have to say about 
their experiences trying to get dental work done in the state. 

- "For my middle girl, McKenzie, she ended up having to have a root canal and that was a day out of school after having 
three appointments to try and find someone," McKensay Vandelicht said.
- "Taking the time off of work to have to drive further away because we don't have enough 
dentists in the area to accommodate everyone's needs," Vandelicht said.  
- "Forty-two percent of our patients are driving from outside the Columbia area to get work done, 
because they don't have the dental care that they need provided in the smaller cities that they are from," 
Parrott, who owns Aspen Dental in Columbia and Jefferson City, said.  
- "Increasing the funding for loan repayment to help areas of decreased access would be a huge help," 
Jacqueline Miller, director of Missouri Oral Health said.
"""

goals = """
- Understand locations of dental providers across the state
- Understand how dental providers move across the state. 
- Deliver data driven guidance for future policy 
"""

with st.container():
    col1, col2, col3 = st.columns(spec=[0.45, 0.1, 0.45])

    with col1:
       st.header("The Problem")
       st.markdown(problem)

    with col2:
       st.header('')

    with col3:
       st.header("Goals")
       st.markdown(goals)

    st.write("\n\n\n")

with st.container():
    st.header("How to use this dashboard")
