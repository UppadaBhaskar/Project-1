# College Management System

A full-stack web application for college faculty to manage student data. Built with Flask (backend), SQLite (database), and React (frontend).

## Features

- **Faculty Authentication**: Registration and login system for faculty members
- **Student Management**: 
  - View list of all students with roll number, name, and section
  - Create new students with confirmation modal
  - View detailed student profiles
  - Update student information (except roll number)
  - Delete students

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Frontend**: React.js with React Router
- **HTTP Client**: Axios

## Setup Instructions

### Prerequisites

- Python 3.7+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Install Node dependencies:
```bash
npm install
```

2. Start the React development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

### Database

The database (`college_management.db`) will be automatically created and initialized with seed data when you first run the Flask application.

**Seed Data:**
- Faculty accounts: `abc/abc123` and `def/abc123`
- Sample student: Roll number `AB23`, Name `Manu`, Section `A`

## Project Structure

```
Project-1/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── package.json          # Node.js dependencies
├── college_management.db # SQLite database
├── public/               # Public assets
│   └── index.html
├── src/                  # React source code
│   ├── App.js           # Main app component with routing
│   ├── App.css
│   ├── index.js         # React entry point
│   ├── index.css
│   └── components/      # React components
│       ├── Login.js
│       ├── Register.js
│       ├── Home.js
│       ├── CreateStudent.js
│       ├── StudentProfile.js
│       └── UpdateStudent.js
└── build/               # Production build (generated)
```

## API Endpoints

### Authentication
- `POST /api/register` - Register new faculty
- `POST /api/login` - Faculty login
- `POST /api/logout` - Logout
- `GET /api/check-auth` - Check authentication status

### Students
- `GET /api/students` - Get all students
- `POST /api/students` - Create new student
- `GET /api/students/<roll_number>` - Get student by roll number
- `PUT /api/students/<roll_number>` - Update student
- `DELETE /api/students/<roll_number>` - Delete student

## Usage

1. Start both backend and frontend servers
2. Navigate to `http://localhost:3000`
3. Register a new faculty account or login with seed credentials
4. View, create, update, or delete students

## Notes

- All routes are protected and require authentication
- Roll number is the primary key and cannot be changed after creation
- Password hashing is implemented for security
- Session-based authentication is used


