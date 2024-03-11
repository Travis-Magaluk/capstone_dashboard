import streamlit as st

st.title("Dental Health in Missouri")
st.header("Please Login to the Database")
import datetime

st.title('Counter Example')
if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.last_updated = datetime.time(0,0)

def update_counter():
    st.session_state.count += st.session_state.increment_value
    st.session_state.last_updated = st.session_state.update_time

with st.form(key='my_form'):
    st.time_input(label='Enter the time', value=datetime.datetime.now().time(), key='update_time')
    st.number_input('Enter a value', value=0, step=1, key='increment_value')
    submit = st.form_submit_button(label='Update', on_click=update_counter)

st.write('Current Count = ', st.session_state.count)
st.write('Last Updated = ', st.session_state.last_updated)


if 'database_password' not in st.session_state:
    st.session_state['database_password'] = 'need updated password'
    st.session_state.user = 'postgres'
    st.session_state.database = 'dentdb'
def update_credentials(password, database, user):
    st.session_state.database_password = password
    st.session_state.database = database
    st.session_state.user = user

with st.form(key="authentication_form"):
    database = st.text_input('Which Database would you like to access?', key='database')
    user = st.text_input("Your Username", key='user')
    userpass = st.text_input('Your Password', type='password', key='database_password')
    st.form_submit_button("Login")