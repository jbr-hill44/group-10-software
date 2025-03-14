# Guide
# Open this file using VS Studio or your preferred IDE
# In VS Studio, click view in the top menu and select Terminal
# run cls to clear the screen
# Then run pip install streamlit and pip install sentence-transformers
# run cls to clear the screen
# Then python -m streamlit run .\matchmaking_demo.py
# This should render the demo
# You can play around by adding more sample projects, use different student interests


import streamlit as st
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')     # instantiate the model

# Streamlit UI
st.title(' 👩‍🎓Academic Matchmaking Demo')
st.subheader('Find the Best Research Match Based on Your Skills')

# Sample User input
student_skills = st.text_area('Enter Your Skills & Research Interests', 'Machine Learning, Data Science, Python')

# Sample project dataset
# This should be replaced with data sourced from the SQL.
projects = ['AI-powered medical diagnosis using deep learning',
            'Climate change modeling using statistical methods',
            'Quantum computing for secure communication',
            'Blockchain technology for academic credentials verification',
           ]

# Compute similarity scores
if st.button('Find Matches'):
    student_embed = model.encode(student_skills, convert_to_tensor=True)     # word embedding (vector)
    project_embeds = model.encode(projects, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(student_embed, project_embeds)     # compute cosine similarity score

    # Display ranked matches
    topn = 2        # number of matches to display
    sorted_indices = similarities.argsort(descending=True)
    st.write(f'### Top {topn} Research Matches:')
    rank = 0
    for idx in sorted_indices[0][:topn]:  # Show top 3 matches
        st.write(f'✅ {rank + 1}. {projects[idx]} (Match Score: {similarities[0, idx] * 100:.2f}%)')
        rank += 1
