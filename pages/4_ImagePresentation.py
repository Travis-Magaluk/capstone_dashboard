import streamlit as st

st.set_page_config(layout="wide")

st.title('Geospatial Analysis')

st.write("Here is how you should use and navigate this page. We hope you will gain this from this page and information. ")

tab1, tab2, tab3 = st.tabs(["Missouri", "St. Louis", "Kansas City"])

with tab1:
    st.image('images/img2.png')
with tab2:
    with st.container():
        col1, col2 = st.columns(spec=[0.5, 0.5])
        with col1:
            st.header('Header for Image 1')
            st.image('images/stl/stl1.png')
        with col2:
            st.header('Header for Image 2')
            st.image('images/stl/stl2.png')
    with st.container():
        col3, col4 = st.columns(spec=[0.5, 0.5])
        with col3:
            st.header('Header for Image 3')
            st.image('images/stl/stl3.png')
        with col4:
            st.write('This is some writeup about the images a;lkgjsadfjwe;lkfj asd;lsda;lfkjasd;lfkjasdf;lj')


with tab3:
    st.image('images/img3.png')

