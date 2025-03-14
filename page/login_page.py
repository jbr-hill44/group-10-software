import streamlit as st
from utils.db_handler import authenticate_user
#from page.matching import  headers
import time

# Pages
def login_page(guest_mode=False):
    st.title(' 👩‍🎓Academic Matchmaking🧑‍🎓')
    st.subheader('Find the Best Research Match Based on Your Skills')
    #headers()[0]
    #headers()[1]

    with st.empty().container(border=True):
        col1, _, col2 = st.columns([10,1,10])
        
        with col1:
            st.write('')
            st.write('')
            # st.video("data/demo.mp4", autoplay=True, loop=True, muted=True)
            st.image('data/logo.jpg')
        
        with col2:
            st.subheader('Login')

            email = st.text_input('E-mail')
            password = st.text_input('Password', type='password')

            if st.button('Login'):
                time.sleep(2)
                if not (email and password):
                    st.error('Please provide email and password')
                elif authenticate_user(email, password):
                    st.session_state['authenticated'] = True
                    st.session_state['page'] = 'app'
                    st.rerun()
                else:
                    st.error('Invalid login credentials')

            if st.button('Sign Up'):
                st.session_state['page'] = 'signup'
                st.rerun()
                
            if guest_mode:
                if st.button('Continue as Guest'):
                    st.session_state['guest_mode'] = True
                    st.session_state['authenticated'] = True
                    st.session_state['page'] = 'app'
                    st.rerun()
