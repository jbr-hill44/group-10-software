import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
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

DATABASE_URL = f'postgresql://{db_params["user"]}:{db_params["password"]}@localhost/{db_params["dbname"]}'
engine = create_engine(DATABASE_URL)

# def create_database():
#     # Connect to the default 'postgres' database to create a new database
#     conn = psycopg2.connect(dbname="postgres", **{k: v for k, v in db_params.items() if k != "dbname"})
#     conn.autocommit = True
#     cursor = conn.cursor()
    
#     # Create the new database
#     cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_params["dbname"])))
    
#     cursor.close()
#     conn.close()

def create_table():
    # Connect to the database
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    """System Prompt
    Create a PostgreSQL table schema for a user management system. The table should have the following columns:

    1. `id`: A primary key of type SERIAL.
    2. `email`: A unique, non-nullable VARCHAR(255) field.
    3. `password`: A non-nullable TEXT field.
    4. `role`: non-nullable VARCHAR(10) field

    Additionally, include the following columns based on user input parameters:

    <extra_input_params> = {
        
    }

    The generated SQL should be a valid `CREATE TABLE` command in PostgreSQL.
    
    output format:
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        hash_password TEXT NOT NULL,
        <extra_input_param> <extra_input_param type> NOT NULL,
    );

    """
    # Create the table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email VARCHAR(255) PRIMARY KEY UNIQUE NOT NULL,
            password TEXT UNIQUE NOT NULL,
            role VARCHAR(10) NOT NULL
        );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    # try:
    #     create_database()
    #     print('Database created successfully.')
    # except psycopg2.Error as e:
    #     print(f'Error creating database: {e}')

    try:
        create_table()
        print('Table created successfully.')
    except psycopg2.Error as e:
        print(f'Error creating table: {e}')
