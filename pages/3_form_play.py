import streamlit as st

values = st.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0))
st.write('Values:', values)


with st.form(key='barchart_params'):
    by = st.selectbox(
        'How would you like to be contacted?',
        ('Email', 'Home phone', 'Mobile phone'))
    minn, maxx = st.slider(label, min_value=0, max_value=df.distance_m.max(), value=None, step=5,
               label_visibility="visible")
    st.form_submit_button(label='Update Barchart')
