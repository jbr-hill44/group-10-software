import streamlit as st
from sentence_transformers import SentenceTransformer, util
#from utils.db_handler import get_projects, get_data
from utils.supa_db_handler import get_projects

def headers():
    TITLE = st.title(' 👩‍🎓Academic Matchmaking🧑‍🎓')
    SUB_TITLE = st.subheader('Find the Best Research Match Based on Your Skills')
    return TITLE, SUB_TITLE

#def get_matching(projects):
def get_matching():
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    # Sample User input
    student_skills = st.text_area('Enter Your Skills & Research Interests (matches through text)', 'healthcare')
    # topics = get_data()['project title'].tolist()
    topics = get_projects()['project_title'].tolist()
    researcher = get_projects()['staff_name'].tolist()
    summaries = get_projects()['summary_expanded'].tolist()
    keywords = get_projects()['key_words'].tolist()

    student_keywords = st.text_area('matches keywords in keyword column', 'Computational statistics')

    if st.button('Find Matches'):
        student_embed = model.encode(student_skills, convert_to_tensor=True)        
        #project_embeds = model.encode(projects, convert_to_tensor=True)
        project_embeds = model.encode(summaries, convert_to_tensor=True)
        similarities_text = util.pytorch_cos_sim(student_embed, project_embeds)

        keywords_embeds = model.encode(keywords, convert_to_tensor=True)
        student_keywords = model.encode(student_keywords, convert_to_tensor=True)
        similarities_keywords = util.pytorch_cos_sim(student_keywords, keywords_embeds)


        similarities = 0.8*similarities_text + 0.2*similarities_keywords


        # Display ranked matches
        topn = 5
        sorted_indices = similarities.argsort(descending=True)
        st.write(f'### Top {topn} Research Matches:')
        rank = 0
        for idx in sorted_indices[0][:topn]:  # Show top n matches
            project_title = topics[idx]
            researcher_name = researcher[idx]
            summary = summaries[idx]
            match_score = similarities[0,idx] * 100
            key = f"show_{idx}"
            st.write(f'✅ {rank + 1}. {project_title} (Match Score: {match_score:.2f}%)')
            with st.expander("View Details"):
                st.write(f"{researcher_name}")
                st.write(f"{summary}")
            rank += 1
        

def user_match(): 
    '''Match a registered user'''      
    projects = get_projects()['project_title'].tolist()  # Projects from DB
    get_matching(projects)                             # Compute similarity scores


def guest_match():
    '''Match a guest'''
    projects = get_projects()['project_title'].tolist()       # Get project titles from db
    get_matching(projects)                                  # Compute similarity scores
            
def match(): 
    '''Match skills'''      
    #projects = get_projects()['project_title'].tolist()  # Projects from DB
    #get_matching(projects)
    get_matching()
