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

def create_roles_table(): #Creates the table that stores the different types of users in the system.

    connection = get_connection() #Opens a connection to the PostgreSQL database.

    cursor = connection.cursor() #Creates a cursor that lets Python send SQL commands to PostgreSQL.

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS roles (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
        """
    ) #Creates the roles table with an automatic ID and a unique required role name.

    connection.commit() #Saves the new table permanently in PostgreSQL.

    cursor.close() #Closes the cursor after the SQL command is finished.

    connection.close() #Closes the database connection.



def add_default_roles(): #Adds the three user roles required by the system.

    connection = get_connection() #Opens a connection to the PostgreSQL database.

    cursor = connection.cursor() #Creates a cursor that lets Python send SQL commands to PostgreSQL.

    cursor.execute(
        """
        INSERT INTO roles (name)
        VALUES
            ('Employee'),
            ('Technician'),
            ('Administrator')
        ON CONFLICT (name) DO NOTHING;
        """
    ) #Adds the required roles and skips any role that already exists.

    connection.commit() #Saves the roles permanently in PostgreSQL.

    cursor.close() #Closes the cursor after the SQL command is finished.

    connection.close() #Closes the database connection.



def create_users_table(): #Creates the table that stores the people who can use the system.

    connection = get_connection() #Opens a connection to the PostgreSQL database.

    cursor = connection.cursor() #Creates a cursor that lets Python send SQL commands to PostgreSQL.

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role_id INTEGER NOT NULL,
            FOREIGN KEY (role_id) REFERENCES roles(id)
        );
        """
    ) #Creates the users table and connects each user to a role stored in the roles table.

    connection.commit() #Saves the new table permanently in PostgreSQL.

    cursor.close() #Closes the cursor after the SQL command is finished.

    connection.close() #Closes the database connection.


def create_ticket_categories_table(): #Creates the table that stores the categories used to organize IT support tickets.

    connection = get_connection() #Opens a connection to the PostgreSQL database.

    cursor = connection.cursor() #Creates a cursor that lets Python send SQL commands to PostgreSQL.

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ticket_categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
        """
    ) #Creates the ticket categories table with an automatic ID and a unique required category name.

    connection.commit() #Saves the new table permanently in PostgreSQL.

    cursor.close() #Closes the cursor after the SQL command is finished.

    connection.close() #Closes the database connection.


def add_default_ticket_categories(): #Adds the four ticket categories required by the system.

    connection = get_connection() #Opens a connection to the PostgreSQL database.

    cursor = connection.cursor() #Creates a cursor that lets Python send SQL commands to PostgreSQL.

    cursor.execute(
        """
        INSERT INTO ticket_categories (name)
        VALUES
            ('Hardware'),
            ('Software'),
            ('Network'),
            ('Account Access')
        ON CONFLICT (name) DO NOTHING;
        """
    ) #Adds the required ticket categories and skips any category that already exists.

    connection.commit() #Saves the ticket categories permanently in PostgreSQL.

    cursor.close() #Closes the cursor after the SQL command is finished.

    connection.close() #Closes the database connection.


def create_priorities_table(): #Creates the table that stores the urgency levels used for IT support tickets.

    connection = get_connection() #Opens a connection to the PostgreSQL database.

    cursor = connection.cursor() #Creates a cursor that lets Python send SQL commands to PostgreSQL.

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS priorities (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
        """
    ) #Creates the priorities table with an automatic ID and a unique required priority name.

    connection.commit() #Saves the new table permanently in PostgreSQL.

    cursor.close() #Closes the cursor after the SQL command is finished.

    connection.close() #Closes the database connection.

def add_default_priorities(): #Adds the four ticket priority levels required by the system.

    connection = get_connection() #Opens a connection to the PostgreSQL database.

    cursor = connection.cursor() #Creates a cursor that lets Python send SQL commands to PostgreSQL.

    cursor.execute(
        """
        INSERT INTO priorities (name)
        VALUES
            ('Low'),
            ('Medium'),
            ('High'),
            ('Critical')
        ON CONFLICT (name) DO NOTHING;
        """
    ) #Adds the required priority levels and skips any priority that already exists.

    connection.commit() #Saves the priorities permanently in PostgreSQL.

    cursor.close() #Closes the cursor after the SQL command is finished.

    connection.close() #Closes the database connection.

def create_ticket_statuses_table(): #Creates the table that stores the progress stages used for IT support tickets.

    connection = get_connection() #Opens a connection to the PostgreSQL database.

    cursor = connection.cursor() #Creates a cursor that lets Python send SQL commands to PostgreSQL.

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ticket_statuses (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
        """
    ) #Creates the ticket statuses table with an automatic ID and a unique required status name.

    connection.commit() #Saves the new table permanently in PostgreSQL.

    cursor.close() #Closes the cursor after the SQL command is finished.

    connection.close() #Closes the database connection.

def add_default_ticket_statuses(): #Adds the four ticket progress stages required by the system.

    connection = get_connection() #Opens a connection to the PostgreSQL database.

    cursor = connection.cursor() #Creates a cursor that lets Python send SQL commands to PostgreSQL.

    cursor.execute(
        """
        INSERT INTO ticket_statuses (name)
        VALUES
            ('Open'),
            ('In Progress'),
            ('Resolved'),
            ('Closed')
        ON CONFLICT (name) DO NOTHING;
        """
    ) #Adds the required ticket statuses and skips any status that already exists.

    connection.commit() #Saves the statuses permanently in PostgreSQL.

    cursor.close() #Closes the cursor after the SQL command is finished.

    connection.close() #Closes the database connection.


if __name__ == "__main__": #Checks if this file is being run directly to set up the database.

    create_roles_table() #Creates the table that stores the different user roles.

    create_users_table() #Creates the table that stores the users and connects them to their roles.

    create_ticket_categories_table() #Creates the table that stores the categories used for support tickets.

    create_priorities_table() #Creates the table that stores the urgency levels used for support tickets.

    create_ticket_statuses_table() #Creates the table that stores the progress stages used for support tickets.


    add_default_roles() #Adds Employee, Technician, and Administrator to the roles table.

    add_default_ticket_categories() #Adds Hardware, Software, Network, and Account Access to the ticket categories table.

    add_default_priorities() #Adds Low, Medium, High, and Critical to the priorities table.

    add_default_ticket_statuses() #Adds Open, In Progress, Resolved, and Closed to the ticket statuses table.


    print("Database foundation created successfully.") #Confirms that the tables and required starter data were created.