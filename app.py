from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='build', static_url_path='')
app.secret_key = 'your-secret-key-change-in-production'
CORS(app, supports_credentials=True)

DATABASE = 'college_management.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Create faculty table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty (
            faculty_id INTEGER PRIMARY KEY AUTOINCREMENT,
            faculty_name VARCHAR NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    ''')
    
    # Create student table with college field
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student (
            roll_number VARCHAR(10) PRIMARY KEY,
            student_name VARCHAR NOT NULL,
            section VARCHAR(5),
            email VARCHAR NOT NULL,
            address VARCHAR,
            phone_number INTEGER NOT NULL,
            college VARCHAR
        )
    ''')
    
    # Check if seed data exists
    cursor.execute('SELECT COUNT(*) as count FROM faculty')
    if cursor.fetchone()['count'] == 0:
        cursor.execute("INSERT INTO faculty(faculty_name, password) VALUES ('abc', ?)", 
                      (generate_password_hash('abc123'),))
        cursor.execute("INSERT INTO faculty(faculty_name, password) VALUES ('def', ?)", 
                      (generate_password_hash('abc123'),))
    
    cursor.execute('SELECT COUNT(*) as count FROM student')
    if cursor.fetchone()['count'] == 0:
        cursor.execute('''
            INSERT INTO student(roll_number, student_name, section, email, address, phone_number, college) 
            VALUES ('AB23', 'Manu', 'A', 'manu@example.com', 'Banglore', 1234567890, 'ABC College')
        ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Auth routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    faculty_name = data.get('faculty_name')
    password = data.get('password')
    
    if not faculty_name or not password:
        return jsonify({'error': 'Faculty name and password are required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if faculty already exists
    cursor.execute('SELECT * FROM faculty WHERE faculty_name = ?', (faculty_name,))
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Faculty name already exists'}), 400
    
    # Hash password and insert
    hashed_password = generate_password_hash(password)
    cursor.execute('INSERT INTO faculty(faculty_name, password) VALUES (?, ?)', 
                  (faculty_name, hashed_password))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Registration successful'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    faculty_name = data.get('faculty_name')
    password = data.get('password')
    
    if not faculty_name or not password:
        return jsonify({'error': 'Faculty name and password are required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM faculty WHERE faculty_name = ?', (faculty_name,))
    faculty = cursor.fetchone()
    conn.close()
    
    if faculty and check_password_hash(faculty['password'], password):
        session['faculty_id'] = faculty['faculty_id']
        session['faculty_name'] = faculty['faculty_name']
        return jsonify({'message': 'Login successful', 'faculty_name': faculty['faculty_name']}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    if 'faculty_id' in session:
        return jsonify({'authenticated': True, 'faculty_name': session.get('faculty_name')}), 200
    return jsonify({'authenticated': False}), 401

# Student routes
@app.route('/api/students', methods=['GET'])
def get_students():
    if 'faculty_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT roll_number, student_name, section FROM student')
    students = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(students), 200

@app.route('/api/students', methods=['POST'])
def create_student():
    if 'faculty_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    roll_number = data.get('roll_number')
    student_name = data.get('student_name')
    section = data.get('section')
    email = data.get('email')
    address = data.get('address')
    phone_number = data.get('phone_number')
    college = data.get('college')
    
    if not all([roll_number, student_name, email, phone_number]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if roll number already exists
    cursor.execute('SELECT * FROM student WHERE roll_number = ?', (roll_number,))
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Roll number already exists'}), 400
    
    cursor.execute('''
        INSERT INTO student(roll_number, student_name, section, email, address, phone_number, college)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (roll_number, student_name, section, email, address, phone_number, college))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Student created successfully'}), 201

@app.route('/api/students/<roll_number>', methods=['GET'])
def get_student(roll_number):
    if 'faculty_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM student WHERE roll_number = ?', (roll_number,))
    student = cursor.fetchone()
    conn.close()
    
    if student:
        return jsonify(dict(student)), 200
    return jsonify({'error': 'Student not found'}), 404

@app.route('/api/students/<roll_number>', methods=['PUT'])
def update_student(roll_number):
    if 'faculty_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    student_name = data.get('student_name')
    section = data.get('section')
    email = data.get('email')
    address = data.get('address')
    phone_number = data.get('phone_number')
    college = data.get('college')
    
    if not all([student_name, email, phone_number]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE student 
        SET student_name = ?, section = ?, email = ?, address = ?, phone_number = ?, college = ?
        WHERE roll_number = ?
    ''', (student_name, section, email, address, phone_number, college, roll_number))
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Student not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Student updated successfully'}), 200

@app.route('/api/students/<roll_number>', methods=['DELETE'])
def delete_student(roll_number):
    if 'faculty_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM student WHERE roll_number = ?', (roll_number,))
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Student not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Student deleted successfully'}), 200

# Serve React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)


