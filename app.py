from flask_wtf.csrf import CSRFProtect #Imports protection against unauthorized form submissions.

import psycopg2 #Imports PostgreSQL errors so duplicate emails can be handled.

from flask import Flask, render_template, request, redirect, url_for, session, flash #Imports tools for forms, navigation, login sessions, and messages.

from database import get_connection #Imports our existing function for connecting to PostgreSQL.

from werkzeug.security import generate_password_hash, check_password_hash #Imports tools for securely hashing and checking passwords.

import os #Imports tools for reading environment variables.

app = Flask(__name__) #Creates the Flask web application.
app.secret_key = os.environ["SECRET_KEY"] #Uses a secret value to protect Flask session cookies.
csrf = CSRFProtect(app) #Enables CSRF protection for form submissions throughout the application.

@app.route("/") #Tells Flask to run the function below when someone visits the home page.
def home(): #Creates the function responsible for displaying the home page.

    connection = get_connection() #Opens a connection to PostgreSQL.

    cursor = connection.cursor() #Creates a cursor for sending SQL commands.

    cursor.execute("SELECT COUNT(*) FROM tickets;") #Counts how many support tickets exist.

    ticket_count = cursor.fetchone()[0] #Gets the number returned by PostgreSQL.

    cursor.close() #Closes the database cursor.

    connection.close() #Closes the database connection.

    return render_template("index.html", ticket_count=ticket_count) #Displays the home page and passes the ticket count to HTML.


@app.route("/register", methods=["GET", "POST"]) #Allows users to open and submit the registration page.
def register(): #Handles new employee registrations.

    if request.method == "POST": #Checks whether the registration form was submitted.

        first_name = request.form.get("first_name", "").strip() #Gets the employee's first name.

        last_name = request.form.get("last_name", "").strip() #Gets the employee's last name.

        email = request.form.get("email", "").strip().lower() #Gets the email address in lowercase.

        password = request.form.get("password", "") #Gets the password entered by the employee.

        if not all([first_name, last_name, email, password]): #Checks that all required fields were completed.

            flash("Please complete all fields.") #Displays a validation message.

            return redirect(url_for("register")) #Returns the user to registration.

        if len(password) < 12: #Requires a password containing at least 12 characters.

            flash("Password must contain at least 12 characters.") #Displays the password requirement.

            return redirect(url_for("register")) #Returns to registration.

        password_hash = generate_password_hash(password) #Converts the password into a secure hash.

        connection = get_connection() #Opens a PostgreSQL connection.

        cursor = connection.cursor() #Creates a cursor for SQL commands.

        try: #Attempts to save the new employee.

            cursor.execute(
                """
                INSERT INTO users (first_name, last_name, email, password_hash, role_id)
                SELECT %s, %s, %s, %s, id
                FROM roles
                WHERE name = 'Employee'
                RETURNING id;
                """,
                (first_name, last_name, email, password_hash)
            ) #Creates the account using the Employee role from the database.

            if cursor.fetchone() is None: #Checks whether the Employee role exists.

                connection.rollback() #Cancels the incomplete transaction.

                flash("Registration is temporarily unavailable.") #Displays a safe error message.

                return redirect(url_for("register")) #Returns to registration.

            connection.commit() #Saves the new user permanently.

        except psycopg2.errors.UniqueViolation: #Handles an email address that already exists.

            connection.rollback() #Cancels the failed database transaction.

            flash("An account with this email already exists.") #Displays an understandable error.

            return redirect(url_for("register")) #Returns to registration.

        finally: #Runs whether registration succeeds or fails.

            cursor.close() #Closes the database cursor.

            connection.close() #Closes the database connection.

        flash("Registration successful.") #Confirms the account was created.

        return redirect(url_for("register")) #Returns to registration until we build login.

    return render_template("register.html") #Displays the registration form.


@app.route("/login", methods=["GET", "POST"]) #Allows users to open and submit the login page.
def login(): #Handles user authentication.

    if request.method == "POST": #Checks whether the login form was submitted.

        email = request.form.get("email", "").strip().lower() #Gets the user's email address.

        password = request.form.get("password", "") #Gets the password entered by the user.

        connection = get_connection() #Opens a connection to PostgreSQL.

        cursor = connection.cursor() #Creates a cursor for SQL commands.

        try: #Ensures database resources are closed after the query.

            cursor.execute(
                """
                SELECT id, first_name, password_hash, role_id
                FROM users
                WHERE email = %s;
                """,
                (email,)
            ) #Finds the account matching the submitted email.

            user = cursor.fetchone() #Retrieves the matching user or None.

        finally: #Runs after the database query.

            cursor.close() #Closes the database cursor.

            connection.close() #Closes the database connection.

        if user and check_password_hash(user[2], password): #Checks the password against its stored hash.

            session.clear() #Removes any existing login session data.

            session["user_id"] = user[0] #Stores the authenticated user's ID.

            session["first_name"] = user[1] #Stores the user's first name.

            session["role_id"] = user[3] #Stores the user's role ID.

            flash("Login successful.") #Displays a confirmation message.

            return redirect(url_for("home")) #Redirects to the home page.

        flash("Invalid email or password.") #Displays a generic error without revealing which field was wrong.

        return redirect(url_for("login")) #Returns to the login page.

    return render_template("login.html") #Displays the login form.


@app.route("/logout", methods=["POST"]) #Allows logged-in users to submit a logout request.
def logout(): #Handles logging the user out.

    session.clear() #Removes the user's login information from the session.

    flash("You have been logged out.") #Displays a logout confirmation.

    return redirect(url_for("login")) #Redirects the user to the login page.


@app.route("/dashboard") #Creates a URL for the user dashboard.
def dashboard(): #Displays a page available only to logged-in users.

    if "user_id" not in session: #Checks whether the user has logged in.

        flash("Please log in to access the dashboard.") #Displays an access message.

        return redirect(url_for("login")) #Sends unauthenticated users to login.

    return render_template("dashboard.html", first_name=session["first_name"]) #Displays the dashboard for the logged-in user.

# Displays the form for creating a support ticket.

# Allows logged-in employees to create support tickets.
@app.route("/tickets/new", methods=["GET", "POST"])
def new_ticket():

    # Redirects visitors who are not logged in.
    if "user_id" not in session:
        flash("Please log in to create a support ticket.")
        return redirect(url_for("login"))

    # Opens a connection to PostgreSQL.
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Retrieves the categories for the dropdown menu.
        cursor.execute(
            "SELECT id, name FROM ticket_categories ORDER BY id;"
        )
        categories = cursor.fetchall()

        # Retrieves the priorities for the dropdown menu.
        cursor.execute(
            "SELECT id, name FROM priorities ORDER BY id;"
        )
        priorities = cursor.fetchall()

        # Checks whether the employee submitted the form.
        if request.method == "POST":

            # Gets the information entered into the form.
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            category_id = request.form.get("category_id", "")
            priority_id = request.form.get("priority_id", "")

            # Prevents empty fields from being submitted.
            if not all([title, description, category_id, priority_id]):
                flash("Please complete all ticket fields.")
                return redirect(url_for("new_ticket"))

            # Checks the maximum title length.
            if len(title) > 255:
                flash("Ticket title must be 255 characters or fewer.")
                return redirect(url_for("new_ticket"))

            # Confirms that the selected category and priority exist.
            valid_categories = {str(item[0]) for item in categories}
            valid_priorities = {str(item[0]) for item in priorities}

            if category_id not in valid_categories or priority_id not in valid_priorities:
                flash("Please select a valid category and priority.")
                return redirect(url_for("new_ticket"))

            # Finds the ID of the Open ticket status.
            cursor.execute(
                "SELECT id FROM ticket_statuses WHERE name = 'Open';"
            )
            status = cursor.fetchone()

            # Stops ticket creation if the Open status is missing.
            if status is None:
                flash("Ticket creation is temporarily unavailable.")
                return redirect(url_for("new_ticket"))

            # Saves the new ticket in PostgreSQL.
            cursor.execute(
                """
                INSERT INTO tickets
                    (title, description, employee_id, category_id, priority_id, status_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    title,
                    description,
                    session["user_id"],
                    int(category_id),
                    int(priority_id),
                    status[0]
                )
            )

            # Retrieves the ID of the newly created ticket.
            ticket_id = cursor.fetchone()[0]

            # Permanently saves the ticket.
            connection.commit()

            # Shows a success message.
            flash(f"Ticket #{ticket_id} created successfully.")

            # Returns to the ticket creation page.
            return redirect(url_for("new_ticket"))

    except Exception:
        # Cancels unfinished database changes if an error occurs.
        connection.rollback()

        # Records the error in the Flask terminal.
        app.logger.exception("Unable to create or load a support ticket.")

        # Shows a safe message without exposing database details.
        flash("Something went wrong. Please try again.")

        return redirect(url_for("dashboard"))

    finally:
        # Closes the database resources.
        cursor.close()
        connection.close()

    # Displays the form when the user first opens the page.
    return render_template(
        "new_ticket.html",
        categories=categories,
        priorities=priorities
    )


# Displays support tickets belonging to the logged-in employee.
@app.route("/tickets")
def view_tickets():

    # Prevents visitors from viewing tickets without logging in.
    if "user_id" not in session:
        flash("Please log in to view your tickets.")
        return redirect(url_for("login"))

    # Connects to PostgreSQL.
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Retrieves only tickets created by the logged-in employee.
        cursor.execute(
            """
            SELECT
                t.id,
                t.title,
                c.name,
                p.name,
                s.name,
                t.created_at
            FROM tickets AS t
            JOIN ticket_categories AS c ON t.category_id = c.id
            JOIN priorities AS p ON t.priority_id = p.id
            JOIN ticket_statuses AS s ON t.status_id = s.id
            WHERE t.employee_id = %s
            ORDER BY t.created_at DESC, t.id DESC;
            """,
            (session["user_id"],)
        )

        # Stores the database results in a Python list.
        tickets = cursor.fetchall()

    finally:
        # Closes the database connection.
        cursor.close()
        connection.close()

    # Sends the tickets to the HTML page.
    return render_template("tickets.html", tickets=tickets)

# Displays the details of one support ticket.
@app.route("/tickets/<int:ticket_id>")
def ticket_details(ticket_id):

    # Prevents visitors from viewing tickets without logging in.
    if "user_id" not in session:
        flash("Please log in to view ticket details.")
        return redirect(url_for("login"))

    # Opens a connection to PostgreSQL.
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Retrieves the ticket only if it belongs to the logged-in employee.
        cursor.execute(
            """
            SELECT
                t.id,
                t.title,
                t.description,
                c.name,
                p.name,
                s.name,
                t.created_at,
                t.updated_at
            FROM tickets AS t
            JOIN ticket_categories AS c ON t.category_id = c.id
            JOIN priorities AS p ON t.priority_id = p.id
            JOIN ticket_statuses AS s ON t.status_id = s.id
            WHERE t.id = %s AND t.employee_id = %s;
            """,
            (ticket_id, session["user_id"])
        )

        # Retrieves one matching ticket, or None if no ticket is found.
        ticket = cursor.fetchone()

    finally:
        # Closes the database resources.
        cursor.close()
        connection.close()

    # Returns a 404 error if the ticket does not exist or belongs to someone else.
    if ticket is None:
        return "Ticket not found.", 404

    # Sends the ticket information to the HTML page.
    return render_template("ticket_details.html", ticket=ticket)

if __name__ == "__main__": #Checks whether this file is being run directly.

    app.run(debug=True) #Starts Flask in development mode so we can test the website.
