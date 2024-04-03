import streamlit as st
from pathlib import Path




tab1, tab2, tab3 = st.tabs(["img1", "img2", "img3"])

with tab1:
    st.image('images/img1.png')
with tab2:
    st.image('images/img2.png')

with tab3:
    st.image('images/img3.png')

