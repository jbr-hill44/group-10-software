from supabase import create_client, Client
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os


def get_supabase_data(topic):
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    response = (
        supabase.table("supervisor_projects")
        .select('staff_name', 'project_title', 'required_skills')
        .contains('key_words', [topic])
        .execute()
    )
    return response
