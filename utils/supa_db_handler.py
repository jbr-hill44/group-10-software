import os
import bcrypt
import pandas as pd
from dotenv import load_dotenv
from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client

load_dotenv()

# Define parameters needed to connect to supabase
supabase_params = {
    "url" : SUPABASE_URL,
    "key" : SUPABASE_KEY
}

# Create a supabase client
supabase: Client = create_client(supabase_params["url"], supabase_params["key"])

def verify_duplicate_user(email):

    check_user = (
        supabase.table("users")
        .select("*")
        .eq('email', email)
        .execute()
    )
    # Will return 0 if there are no matching records
    count = len(check_user.data)

    return count > 0


def authenticate_user(email, password):

    # Retrieve the stored hashed password for the user
    get_pwrd = (
        supabase.table("users")
        .select('password')
        .eq('email',email)
        .execute()
    )
    stored_hashed_password = get_pwrd.data[0]

    # Check if a user with the given email was found
    if stored_hashed_password is None:
        return False

    stored_hashed_password = stored_hashed_password["password"]  # Extract the hash from the tuple

    # Compare the provided password with the stored hashed password
    return bcrypt.checkpw(password.encode(), stored_hashed_password.encode())



def save_user(email, password, role):

    # Hash the password before saving
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')

    create_user = (
        supabase.table("users")
        .insert({"email": email, "password": hashed_password, "role": role})
        .execute()
    )


def get_users():

    return_users = (
        supabase.table("users")
        .select("*")
        .execute()
    )

    users_tuples = [tuple(user.values()) for user in return_users.data]

    return users_tuples

# def get_projects():
#     conn = psycopg2.connect(**db_params)
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM projects")
#     projects = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     return projects

def get_projects():
    projects = (
        supabase.table("supervisor_projects")
        .select("*")
        .execute()
    )
    df = pd.DataFrame(projects.data)
    return df

#Currently unused but needs updating
# def get_data():
#     df = pd.read_excel('./data/projects.xlsx', header = 0, sheet_name = 'Suggested Projects 2025')
#     for col in list(df):
#         df[col] = df[col].apply(lambda x: 'a' if x == '' or x == ' ' else x)
#     df['objectives'] = df['objectives'].fillna('a')
#     df['description'] = df['project title'] + ' ' + df['required skills'] + ' ' + df['objectives']
#     return df
