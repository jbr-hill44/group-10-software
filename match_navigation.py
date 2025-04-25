import streamlit as st
from page.login_page import login_page
from page.signup_page import signup_page
from page.app import app_page
from page.all_projects import  all_projects
from utils.init_session import init_session, reset_session

init_session()

# email and password required for authentication
st.session_state['extra_input_params'] = {
    'Email':'text',
    'Password':'text',
}
for input_param in st.session_state['extra_input_params'].keys():
    if input_param not in st.session_state:
        st.session_state[input_param] = None

# display the app page for authenticated users 
if st.session_state['authenticated']:
    app_page()
else:
    # display login UI with guest option
    if st.session_state['page'] == 'login':
        reset_session()
        login_page(guest_mode=True)

    # display signup UI when requested by user
    elif st.session_state['page'] == 'signup':
        signup_page(
            extra_input_params=True,
            confirmPass = True
        )
# get all projects from DB
if st.session_state['page'] == 'database':
    all_projects()
