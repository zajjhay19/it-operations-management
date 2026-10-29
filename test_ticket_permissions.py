
# Imports the Flask application for testing.
from app import app

# Creates a simulated browser.
client = app.test_client()

# Temporarily disables CSRF for this isolated test.
app.config["WTF_CSRF_ENABLED"] = False

# Simulates a logged-in Technician (User ID 4).
with client.session_transaction() as session:
    session["user_id"] = 4
    session["first_name"] = "Test"
    session["role_id"] = 2

# Attempts to change Ticket #1, which is not assigned to User ID 4.
response = client.post(
    "/technician/tickets/1/status",
    data={"status_id": "2"}
)

# Displays the HTTP response.
print("HTTP status:", response.status_code)

# Checks that the ticket was not updated.
from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute(
    "SELECT status_id, technician_id FROM tickets WHERE id = 1;"
)

ticket = cursor.fetchone()

print("Ticket #1 status ID:", ticket[0])
print("Ticket #1 technician ID:", ticket[1])

cursor.close()
connection.close()

# Verifies that the unauthorized change was rejected.
assert ticket[0] == 1
assert ticket[1] is None

print("PASS: Technician cannot update an unassigned ticket.")

