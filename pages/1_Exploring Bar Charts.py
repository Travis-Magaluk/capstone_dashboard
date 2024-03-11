import streamlit as st
import matplotlib.pyplot as plt
st.set_page_config(layout="wide")

conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM all_moves;', ttl="10m")

def update_chart():


with st.form(key='barchart_params'):
    by = st.selectbox(
        'How would you like to be contacted?',
        ('Email', 'Home phone', 'Mobile phone'))
    minn, maxx = st.slider(label, min_value=0, max_value=df.distance_m.max(), value=None, step=5,
               label_visibility="visible")
    st.form_submit_button(label='Update Barchart', on_click=update_chart)

fig = px.bar(long_df, x="nation", y="count", color="medal", title="Long-Form Input")
fig.show()