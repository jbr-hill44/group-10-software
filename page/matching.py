import streamlit as st
from sentence_transformers import SentenceTransformer, util
from utils.db_handler import get_projects, get_data

def headers():
    TITLE = st.title(' 👩‍🎓Academic Matchmaking🧑‍🎓')
    SUB_TITLE = st.subheader('Find the Best Research Match Based on Your Skills')
    return TITLE, SUB_TITLE

def get_matching(projects):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    # Sample User input
    student_skills = st.text_area('Enter Your Skills & Research Interests', 'Machine Learning, Data Science, Python')
    # topics = get_data()['project title'].tolist()
    topics = get_projects()['project title'].tolist()

    if st.button('Find Matches'):
        student_embed = model.encode(student_skills, convert_to_tensor=True)        
        project_embeds = model.encode(projects, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(student_embed, project_embeds)

        # Display ranked matches
        topn = 5
        sorted_indices = similarities.argsort(descending=True)
        st.write(f'### Top {topn} Research Matches:')
        rank = 0
        for idx in sorted_indices[0][:topn]:  # Show top n matches
            #st.write(f'✅ {rank + 1}. {projects[idx]} (Match Score: {similarities[0, idx] * 100:.2f}%)')
            st.write(f'✅ {rank + 1}. {topics[idx]} (Match Score: {similarities[0, idx] * 100:.2f}%)')
            rank += 1
        

def user_match(): 
    '''Match a registered user'''      
    projects = get_projects()['description'].tolist()  # Projects from DB
    get_matching(projects)                             # Compute similarity scores


def guest_match():
    '''Match a guest'''
    #projects = get_data()['description'].tolist()       # Get project titles from table
    projects = get_projects()['description'].tolist()       # Get project titles from db
    get_matching(projects)                                  # Compute similarity scores
            
def match(): 
    '''Match skills'''      
    projects = get_projects()['description'].tolist()  # Projects from DB
    get_matching(projects)
