import streamlit as st
#from utils.db_handler import get_users
from utils.supa_db_handler import get_users
from utils.init_session import reset_session
from page.matching import guest_match, user_match, match
# from page.matching import headers
from utils.supa_db_handler import get_projects



 # Streamlit UI   
def app_page():
    with st.sidebar:
        if st.session_state['guest_mode']:
            st.subheader('Guest Mode')
            
            if st.button('Login'):
                reset_session()
                st.rerun()
                
        elif st.button('Logout'):
            reset_session()
            st.rerun()

    # Streamlit UI   
    st.title(' 👩‍🎓Academic Matchmaking🧑‍🎓')
    st.subheader('Find the Best Research Match Based on Your Skills')
    #headers()[0]
    #headers()[1]

    ###To see user table on page###
    #users = get_users()
    #if users:
    #    st.table(users)

    if st.session_state['guest_mode']:
        match()
    

    elif st.session_state['authenticated']:
        match()

    ### Project database link ###
    st.title("Project Database")
    if st.button("Project Database"):
        st.session_state['page'] = 'database'




