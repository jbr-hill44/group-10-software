import streamlit as st
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
import bcrypt
import pandas as pd
from sqlalchemy import create_engine
load_dotenv()

# Database connection parameters
db_params = {
    "dbname":  os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

# Connect to the DB
DATABASE_URL = f'postgresql://{db_params["user"]}:{db_params["password"]}@localhost/{db_params["dbname"]}'
engine = create_engine(DATABASE_URL)

def verify_duplicate_user(email):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count > 0


def authenticate_user(email, password):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Retrieve the stored hashed password for the user
    cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
    stored_hashed_password = cursor.fetchone()

    cursor.close()
    conn.close()

    # Check if a user with the given email was found
    if stored_hashed_password is None:
        return False

    stored_hashed_password = stored_hashed_password[0]  # Extract the hash from the tuple

    # Compare the provided password with the stored hashed password
    return bcrypt.checkpw(password.encode(), stored_hashed_password.encode())



def save_user(email, password, role):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Hash the password before saving
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')

    # Base columns and values
    columns = ['email', 'password', 'role']
    values = [email, hashed_password, role]

    # Add extra input params to the columns and values lists
    # for key in extra_input_params.keys():
    #     columns.append(key)
    #     values.append(st.session_state[f'{key}'])

    # Dynamically build the SQL query
    columns_str = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(values))

    query = sql.SQL("INSERT INTO users ({}) VALUES ({})").format(
        sql.SQL(columns_str),
        sql.SQL(placeholders)
    )

    # Execute the query
    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()


def get_users():
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users

# def get_projects():
#     conn = psycopg2.connect(**db_params)
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM projects")
#     projects = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     return projects

def get_projects():
    projects = pd.read_sql_query('SELECT * FROM projects;', engine)
    return projects

def get_data():
    df = pd.read_excel('./data/projects.xlsx', header = 0, sheet_name = 'Suggested Projects 2025')
    for col in list(df):
        df[col] = df[col].apply(lambda x: 'a' if x == '' or x == ' ' else x)
    df['objectives'] = df['objectives'].fillna('a')
    df['description'] = df['project title'] + ' ' + df['required skills'] + ' ' + df['objectives']
    return df
