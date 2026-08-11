import os #Imports tools that let Python read database settings stored in the environment.

import psycopg2 #Imports the PostgreSQL tool that lets Python communicate with the database.

from dotenv import load_dotenv #Imports the tool that loads values stored inside the .env file.


load_dotenv() #Loads the database settings from the .env file.

def get_connection(): #Creates a function that opens a connection to the PostgreSQL database.

    connection = psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT")
    ) #Connects Python to PostgreSQL using the settings stored in the environment.

    return connection #Returns the open database connection so other parts of the application can use it.


if __name__ == "__main__": #Checks if this file is being run directly for testing.

    connection = get_connection() #Opens a connection to the PostgreSQL database.

    print("PostgreSQL connection successful.") #Confirms that the database connection worked.

    connection.close() #Closes the database connection after the test.