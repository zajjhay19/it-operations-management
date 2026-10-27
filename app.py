
from flask import Flask, render_template #Imports Flask to create the application and render_template to display HTML pages.

from database import get_connection #Imports our existing function for connecting to PostgreSQL.


app = Flask(__name__) #Creates the Flask web application.


@app.route("/") #Tells Flask to run the function below when someone visits the home page.
def home(): #Creates the function responsible for displaying the home page.

    connection = get_connection() #Opens a connection to PostgreSQL.

    cursor = connection.cursor() #Creates a cursor for sending SQL commands.

    cursor.execute("SELECT COUNT(*) FROM tickets;") #Counts how many support tickets exist.

    ticket_count = cursor.fetchone()[0] #Gets the number returned by PostgreSQL.

    cursor.close() #Closes the database cursor.

    connection.close() #Closes the database connection.

    return render_template("index.html", ticket_count=ticket_count) #Displays the home page and passes the ticket count to HTML.


if __name__ == "__main__": #Checks whether this file is being run directly.

    app.run(debug=True) #Starts Flask in development mode so we can test the website.
