from supabase import create_client, Client
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os


# Load environment variables from .env
load_dotenv()

# Get credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Data import
projects = pd.read_csv("/Users/jameshill/Documents/Python Stuff/Expanded Dissertation topics - Cleaned.csv", lineterminator="\n")
## DATA CLEANING ##
# Remove any trailing whitespace
projects = projects.applymap(lambda x: x.strip() if isinstance(x, str) else x)
# Format key word column properly
projects["Key words\r"] = projects["Key words\r"].apply(lambda x: x.split("\n") if isinstance(x, str) else x)
# Remove NaNs and Infs as supabase doesn't like them
projects = projects.replace({np.nan: None, np.inf: None, -np.inf: None})
# Rename columns to align with database
projects.columns = ['staff_id', 'staff_name', 'project_id', 'project_title', 'required_skills',
                    'objectives_deliverables', 'summary_expanded', 'key_words']

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Convert DataFrame to list of dictionaries
records = projects.to_dict(orient="records")

# Insert DataFrame records into Supabase
response = supabase.from_("supervisor_projects").insert(records).execute()
