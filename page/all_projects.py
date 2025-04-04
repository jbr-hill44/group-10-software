import streamlit as st
import pandas as pd
from utils.supa_db_handler import get_projects

def all_projects():
    project_data = pd.DataFrame(get_projects())

    # Sidebar filter
    st.sidebar.title("Filter Projects")
    all_keywords = ['Data Analysis',
        'Data Mining',
        'Web Development',
        'Cloud Computing',
        'Big Data',
        'E-Commerce',
        'Finance',
        'UX/UI Design',
        'Mobile Application Development',
        'Blockchain',
        'Cryptography',
        'Cybersecurity',
        'Internet of Things (IoT)',
        'Data Visualization',
        'Natural Language Processing (NLP)',
        'Mathematical Modelling',
        'Statistics',
        'Neural Networks',
        'Computer Vision',
        'Autonomous Vehicles',
        'Machine Learning',
        'Deep Learning',
        'Artificial Intelligence',
        'Software Engineering',
        'Robotics',
        'Human-Computer Interaction (HCI)',
        'Game Development',
        'Virtual Reality (VR)',
        'Augmented Reality (AR)',
        'Network Security',
        'Database Management',
        'Distributed Systems',
        'Parallel Computing',
        'Cloud Security',
        'Bioinformatics',
        'Computational Biology',
        'Ethical Hacking',
        'Smart Cities',
        'Digital Transformation',
        'Edge Computing',
        'Healthcare']
    selected_keywords = st.sidebar.multiselect("Select Keywords", all_keywords)

    # Filter logic
    def filter_projects(data, selected_keywords):
        if not selected_keywords:
            return project_data
        return project_data[project_data['key_words'].apply(lambda k: any(kw in k for kw in selected_keywords))]

    filtered_projects = filter_projects(project_data, selected_keywords)

    # Pagination logic
    page_number = st.sidebar.number_input("Page Number", min_value=1, max_value=(len(filtered_projects) // 10) + 1,
                                          value=1)
    start_index = (page_number - 1) * 10
    end_index = start_index + 10
    paginated_projects = filtered_projects.iloc[start_index:end_index]

    st.title("--------------")

    for index, row in paginated_projects.iterrows():
        if st.button(row['project_title']):
            st.session_state['selected_project'] = row

    # Display detailed view
    if 'selected_project' in st.session_state:
        project = st.session_state['selected_project']
        st.header(project['project_title'])
        st.write(project['summary_expanded'])

