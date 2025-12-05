# College Management System

A Flask-based web application for college faculty to manage student data. Faculty can register, login, view student lists, create new students, view profiles, edit student information, and delete students.

## Features

- **Faculty Authentication**
  - Registration page for new faculty members
  - Login page for existing faculty members
  - Password validation (max 12 characters)

- **Student Management**
  - View list of all students with roll number, name, and section
  - Create new students with confirmation modal
  - View detailed student profiles
  - Edit student information (except roll number)
  - Delete students with confirmation dialog

## Database Schema

### Faculty Table
- `faculty_id` (INTEGER PRIMARY KEY)
- `faculty_name` (VARCHAR NOT NULL)
- `password` (VARCHAR(12) NOT NULL)

### Student Table
- `roll_number` (VARCHAR(10) PRIMARY KEY)
- `student_name` (VARCHAR NOT NULL)
- `section` (VARCHAR(5))
- `email` (VARCHAR NOT NULL)
- `address` (VARCHAR)
- `phone_number` (INTEGER NOT NULL)
- `college` (VARCHAR)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Default Credentials

The database is seeded with the following faculty accounts:
- Username: `abc`, Password: `abc123`
- Username: `def`, Password: `abc123`

## Project Structure

```
Project-1/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── college_management.db  # SQLite database (created on first run)
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   ├── create_student.html
│   ├── profile.html
│   └── edit_student.html
└── static/               # Static files
    ├── style.css         # CSS styles
    └── script.js         # JavaScript for modals and interactions
```

## Usage

1. **Registration/Login**: Start by registering a new faculty account or logging in with existing credentials.

2. **View Students**: After logging in, you'll see the home page with a list of all students.

3. **Create Student**: Click "Create Student" button, fill in the form, and confirm the creation.

4. **View Profile**: Click "View Profile" on any student row to see detailed information.

5. **Edit Student**: From the profile page, click "Edit" to modify student details (roll number cannot be changed).

6. **Delete Student**: From the profile page, click the delete icon and confirm the deletion.

## Notes

- Sessions are not yet implemented (as per requirements)
- The database is automatically initialized with seed data on first run
- All forms include validation for required fields
- Confirmation modals prevent accidental actions

