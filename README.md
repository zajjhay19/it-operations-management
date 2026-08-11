# IT Operations Management System

A backend-focused IT Operations Management System built with Python, Flask, and PostgreSQL.

The application is being developed to manage IT support tickets, users, technicians, company IT assets, ticket assignments, priorities, statuses, and operational data from one centralized system.

This project is part of my backend software development portfolio and is designed to demonstrate practical experience with Python, Flask, PostgreSQL, SQL, relational database design, authentication, CRUD operations, backend business logic, data visualization, testing, and deployment.

---

## Project Status

**Version:** 0.1

**Status:** 🚧 In Development

### Current Progress

**Push 1 — Project Foundation:** ✅ Complete

Completed:

- Python project structure
- Python virtual environment
- Flask installation
- PostgreSQL 18 installation
- PostgreSQL database creation
- Python-to-PostgreSQL connection
- Environment variable configuration
- Database credentials protected using `.env`
- Git configuration
- GitHub repository setup
- Python dependencies stored in `requirements.txt`

---

## Project Goal

The goal of this project is to build a complete IT operations platform that can manage the daily workflow of an internal IT department.

The finished application will allow:

- Employees to submit IT support tickets
- Technicians to receive and manage assigned tickets
- Administrators to manage users, tickets, and IT assets
- Tickets to be organized by category
- Tickets to be ranked by priority
- Ticket progress to be tracked using statuses
- Technicians to add updates to tickets
- Company IT equipment to be tracked
- IT assets to be assigned to employees
- Operational information to be displayed through a dashboard

---

## Planned System Roles

The system will contain three user roles:

### Employee

Employees will be able to:

- Log in
- Create support tickets
- View their submitted tickets
- View ticket progress
- View ticket updates
- View IT assets assigned to them

### Technician

Technicians will be able to:

- Log in
- View assigned tickets
- Update ticket statuses
- Work with ticket priorities
- Add comments and updates
- Resolve IT support tickets
- View asset information

### Administrator

Administrators will be able to:

- Manage users
- Manage technicians
- Manage tickets
- Assign tickets
- Manage IT assets
- Assign assets to employees
- View system-wide operational information

---

## Planned Ticket Management

IT support tickets will contain:

- Ticket ID
- Title
- Description
- Employee
- Category
- Priority
- Status
- Assigned technician
- Date created
- Date updated

### Ticket Categories

The system will use:

- Hardware
- Software
- Network
- Account Access

### Ticket Priorities

The system will use:

- Low
- Medium
- High
- Critical

### Ticket Statuses

The ticket workflow will use:

```text
Open
  ↓
In Progress
  ↓
Resolved
  ↓
Closed
```

---

## Planned Asset Management

The system will track company IT equipment.

Asset types:

- Laptop
- Monitor
- Phone
- Printer
- Server

Each asset will store information including:

- Asset ID
- Asset type
- Manufacturer
- Model
- Serial number
- Status

Asset assignments will connect equipment to employees and preserve assignment history.

---

## Planned Database Structure

The PostgreSQL database will contain:

```text
roles
users
ticket_categories
priorities
ticket_statuses
tickets
ticket_comments
assets
asset_assignments
```

The tables will be connected using primary keys and foreign keys.

The planned relationships are:

```text
Roles
  ↓
Users
  │
  ├───────────────┐
  ↓               ↓
Tickets       Asset Assignments
  ↓               ↓
Comments         Assets

Tickets
  ├── Category
  ├── Priority
  ├── Status
  ├── Employee
  └── Technician
```

---

## Planned Application Flow

```text
Employee uses website
        ↓
Flask receives request
        ↓
Python runs backend logic
        ↓
PostgreSQL stores or retrieves information
        ↓
Flask sends information to Jinja2
        ↓
User sees the updated webpage
```

A normal support-ticket workflow will be:

```text
Employee submits IT problem
        ↓
Ticket is stored in PostgreSQL
        ↓
Ticket receives category and priority
        ↓
Technician is assigned
        ↓
Technician begins work
        ↓
Technician adds updates
        ↓
Problem is resolved
        ↓
Ticket is closed
```

---

## Technology Stack

### Backend

- Python 3
- Flask

### Database

- PostgreSQL 18
- psycopg2-binary

### Configuration

- python-dotenv
- Environment variables

### Frontend

Planned:

- HTML5
- CSS3
- Bootstrap 5
- Jinja2
- Chart.js

### Testing

Planned:

- pytest

### Development Tools

- Git
- GitHub
- Visual Studio Code
- PowerShell
- PostgreSQL Command Line Tools

---

## Current Project Structure

```text
it-operations-management/
│
├── static/
├── templates/
├── venv/
│
├── .env
├── .gitignore
├── app.py
├── database.py
├── project_design.md
├── README.md
└── requirements.txt
```

The `.env` and `venv` files are excluded from Git using `.gitignore`.

---

## PostgreSQL Connection

The application uses `psycopg2` to communicate with PostgreSQL.

Database credentials are stored inside a `.env` file instead of being written directly inside the Python source code.

The application reads:

```text
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
```

`database.py` uses these environment variables to create the PostgreSQL connection.

The Python-to-PostgreSQL connection has been successfully tested.

---

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/zajjhay19/it-operations-management.git
```

Enter the project:

```bash
cd it-operations-management
```

---

### 2. Create a Virtual Environment

```bash
py -m venv venv
```

Activate it in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

---

### 3. Install Python Dependencies

```bash
python -m pip install -r requirements.txt
```

---

### 4. Install PostgreSQL

On Windows, PostgreSQL 18 can be installed using WinGet:

```powershell
winget install --id PostgreSQL.PostgreSQL.18 -e --source winget
```

Verify the installation:

```powershell
psql --version
```

Expected version:

```text
psql (PostgreSQL) 18.x
```

If `psql` is installed but is not recognized by the terminal, add the PostgreSQL `bin` directory to the Windows PATH:

```text
C:\Program Files\PostgreSQL\18\bin
```

---

### 5. Create the PostgreSQL Database

Connect to PostgreSQL:

```bash
psql -U postgres -p 5432
```

Create the database:

```sql
CREATE DATABASE it_operations_management;
```

Exit PostgreSQL:

```text
\q
```

---

### 6. Configure Environment Variables

Create a `.env` file in the project root:

```text
DB_NAME=it_operations_management
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD
DB_HOST=localhost
DB_PORT=5432
```

Replace `YOUR_POSTGRES_PASSWORD` with the PostgreSQL password configured on your computer.

Never commit the `.env` file to GitHub.

---

### 7. Test the Database Connection

Run:

```bash
python database.py
```

A successful connection displays:

```text
PostgreSQL connection successful.
```

---

## Development Roadmap

### Push 1 — Project Foundation ✅

- Project structure
- Virtual environment
- Flask
- PostgreSQL
- psycopg2
- python-dotenv
- Environment variables
- Database connection
- Git and GitHub setup

### Push 2 — Database Foundation

- Roles
- Users
- Ticket categories
- Priorities
- Ticket statuses

### Push 3 — Ticket Database

- Tickets
- Ticket comments
- Database relationships

### Push 4 — Asset Database

- Assets
- Asset assignments

### Push 5 — Flask Foundation

- Flask application structure
- Routes
- Templates
- Database integration

### Push 6 — Authentication

- Login
- Logout
- Password hashing
- User roles
- Permissions

### Push 7 — Ticket Creation and Viewing

- Create tickets
- View tickets
- Ticket details

### Push 8 — Ticket Management

- Technician assignment
- Priority management
- Status management

### Push 9 — Ticket History

- Comments
- Technician updates
- Ticket history

### Push 10 — Asset Management

- Add assets
- View assets
- Assign assets
- Track assignments

### Push 11 — Operations Dashboard

- Ticket statistics
- Priority statistics
- Status statistics
- Technician workload
- Asset statistics
- Charts

### Push 12 — Search, Filtering, and Validation

- Ticket search
- Ticket filters
- Form validation
- Error handling

### Push 13 — User Interface

- Bootstrap
- Responsive design
- Navigation
- Dashboard styling

### Push 14 — Testing and Cleanup

- pytest
- Backend tests
- Edge-case testing
- Code cleanup

### Push 15 — Portfolio Release

- Deployment
- Screenshots
- Final README
- Final testing
- Portfolio presentation

---

## Current Development Progress

```text
Push 1 / 15

[█░░░░░░░░░░░░░░]

Project Foundation: Complete
Database Foundation: Next
```

---

## Security

The project keeps database credentials outside the source code using environment variables.

The following files and folders are excluded from Git:

```text
.env
venv/
__pycache__/
*.pyc
```

Passwords and other private credentials should never be committed to the repository.

---

## Author

**Zajae Hayles**

Backend Software Developer

GitHub:  
https://github.com/zajjhay19

---

## License

This project was created for educational purposes and as part of my backend software development portfolio.
