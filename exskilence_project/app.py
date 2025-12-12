from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production
CORS(app)  # Enable CORS for React frontend

DATABASE = 'college_management.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create faculty table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty (
            faculty_id INTEGER PRIMARY KEY AUTOINCREMENT,
            faculty_name VARCHAR NOT NULL,
            password VARCHAR(12) NOT NULL
        )
    ''')
    
    # Create student table with college column
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
    
    # Add college column if it doesn't exist (migration for existing databases)
    try:
        cursor.execute('ALTER TABLE student ADD COLUMN college VARCHAR')
    except sqlite3.OperationalError:
        # Column already exists, ignore
        pass
    
    # Check if seed data exists
    cursor.execute('SELECT COUNT(*) FROM faculty')
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO faculty(faculty_name, password) VALUES ('abc', 'abc123')")
        cursor.execute("INSERT INTO faculty(faculty_name, password) VALUES ('def', 'abc123')")
    
    cursor.execute('SELECT COUNT(*) FROM student')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO student(roll_number, student_name, section, email, address, phone_number, college)
            VALUES ('AB23', 'Manu', 'A', 'manu@example.com', 'Banglore', 1234567890, 'ABC College')
        ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        faculty_name = request.form.get('username')
        password = request.form.get('password')
        
        if not faculty_name or not password:
            flash('Please fill in all fields', 'error')
            return render_template('register.html')
        
        if len(password) > 12:
            flash('Password must be 12 characters or less', 'error')
            return render_template('register.html')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if faculty already exists
        cursor.execute('SELECT * FROM faculty WHERE faculty_name = ?', (faculty_name,))
        if cursor.fetchone():
            conn.close()
            flash('Faculty name already exists', 'error')
            return render_template('register.html')
        
        # Insert new faculty
        cursor.execute('INSERT INTO faculty(faculty_name, password) VALUES (?, ?)', (faculty_name, password))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        faculty_name = request.form.get('username')
        password = request.form.get('password')
        
        if not faculty_name or not password:
            flash('Please fill in all fields', 'error')
            return render_template('login.html')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM faculty WHERE faculty_name = ? AND password = ?', (faculty_name, password))
        faculty = cursor.fetchone()
        conn.close()
        
        if faculty:
            # In future, we'll use sessions here
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/home')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT roll_number, student_name, section FROM student ORDER BY roll_number')
    students = cursor.fetchall()
    conn.close()
    return render_template('home.html', students=students)

@app.route('/create_student', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        roll_number = request.form.get('roll_number')
        student_name = request.form.get('student_name')
        section = request.form.get('section')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        college = request.form.get('college')
        address = request.form.get('address')
        
        if not all([roll_number, student_name, email, phone_number]):
            flash('Please fill in all required fields', 'error')
            return render_template('create_student.html')
        
        try:
            phone_number = int(phone_number)
        except ValueError:
            flash('Phone number must be a valid number', 'error')
            return render_template('create_student.html')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if roll number already exists
        cursor.execute('SELECT * FROM student WHERE roll_number = ?', (roll_number,))
        if cursor.fetchone():
            conn.close()
            flash('Roll number already exists', 'error')
            return render_template('create_student.html')
        
        cursor.execute('''
            INSERT INTO student(roll_number, student_name, section, email, address, phone_number, college)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (roll_number, student_name, section, email, address, phone_number, college))
        
        conn.commit()
        conn.close()
        
        flash('Student created successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('create_student.html')

@app.route('/student/<roll_number>')
def student_profile(roll_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM student WHERE roll_number = ?', (roll_number,))
    student = cursor.fetchone()
    conn.close()
    
    if not student:
        flash('Student not found', 'error')
        return redirect(url_for('home'))
    
    return render_template('profile.html', student=student)

@app.route('/student/<roll_number>/edit', methods=['GET', 'POST'])
def edit_student(roll_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        section = request.form.get('section')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        college = request.form.get('college')
        address = request.form.get('address')
        
        if not all([student_name, email, phone_number]):
            flash('Please fill in all required fields', 'error')
            cursor.execute('SELECT * FROM student WHERE roll_number = ?', (roll_number,))
            student = cursor.fetchone()
            conn.close()
            return render_template('edit_student.html', student=student)
        
        try:
            phone_number = int(phone_number)
        except ValueError:
            flash('Phone number must be a valid number', 'error')
            cursor.execute('SELECT * FROM student WHERE roll_number = ?', (roll_number,))
            student = cursor.fetchone()
            conn.close()
            return render_template('edit_student.html', student=student)
        
        cursor.execute('''
            UPDATE student 
            SET student_name = ?, section = ?, email = ?, address = ?, phone_number = ?, college = ?
            WHERE roll_number = ?
        ''', (student_name, section, email, address, phone_number, college, roll_number))
        
        conn.commit()
        conn.close()
        
        flash('Student updated successfully!', 'success')
        return redirect(url_for('home'))
    
    cursor.execute('SELECT * FROM student WHERE roll_number = ?', (roll_number,))
    student = cursor.fetchone()
    conn.close()
    
    if not student:
        flash('Student not found', 'error')
        return redirect(url_for('home'))
    
    return render_template('edit_student.html', student=student)

@app.route('/student/<roll_number>/delete', methods=['POST'])
def delete_student(roll_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM student WHERE roll_number = ?', (roll_number,))
    conn.commit()
    conn.close()
    
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    faculty_name = data.get('username')
    password = data.get('password')
    
    if not faculty_name or not password:
        return jsonify({'success': False, 'message': 'Please fill in all fields'}), 400
    
    if len(password) > 12:
        return jsonify({'success': False, 'message': 'Password must be 12 characters or less'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if faculty already exists
    cursor.execute('SELECT * FROM faculty WHERE faculty_name = ?', (faculty_name,))
    if cursor.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': 'Faculty name already exists'}), 400
    
    # Insert new faculty
    cursor.execute('INSERT INTO faculty(faculty_name, password) VALUES (?, ?)', (faculty_name, password))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Registration successful! Please login.'}), 200

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    faculty_name = data.get('username')
    password = data.get('password')
    
    if not faculty_name or not password:
        return jsonify({'success': False, 'message': 'Please fill in all fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM faculty WHERE faculty_name = ? AND password = ?', (faculty_name, password))
    faculty = cursor.fetchone()
    conn.close()
    
    if faculty:
        return jsonify({
            'success': True, 
            'message': 'Login successful!',
            'faculty_id': faculty['faculty_id'],
            'faculty_name': faculty['faculty_name']
        }), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

# API endpoints for student operations
@app.route('/api/students', methods=['GET'])
def api_get_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT roll_number, student_name, section FROM student ORDER BY roll_number')
    students = cursor.fetchall()
    conn.close()
    
    students_list = [dict(row) for row in students]
    return jsonify({'success': True, 'students': students_list}), 200

@app.route('/api/students/<roll_number>', methods=['GET'])
def api_get_student(roll_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM student WHERE roll_number = ?', (roll_number,))
    student = cursor.fetchone()
    conn.close()
    
    if not student:
        return jsonify({'success': False, 'message': 'Student not found'}), 404
    
    return jsonify({'success': True, 'student': dict(student)}), 200

@app.route('/api/students', methods=['POST'])
def api_create_student():
    data = request.get_json()
    roll_number = data.get('roll_number')
    student_name = data.get('student_name')
    section = data.get('section', '')
    phone_number = data.get('phone_number')
    email = data.get('email')
    college = data.get('college', '')
    address = data.get('address', '')
    
    if not all([roll_number, student_name, email, phone_number]):
        return jsonify({'success': False, 'message': 'Please fill in all required fields'}), 400
    
    try:
        phone_number = int(phone_number)
    except ValueError:
        return jsonify({'success': False, 'message': 'Phone number must be a valid number'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if roll number already exists
    cursor.execute('SELECT * FROM student WHERE roll_number = ?', (roll_number,))
    if cursor.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': 'Roll number already exists'}), 400
    
    cursor.execute('''
        INSERT INTO student(roll_number, student_name, section, email, address, phone_number, college)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (roll_number, student_name, section, email, address, phone_number, college))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Student created successfully!'}), 201

@app.route('/api/students/<roll_number>', methods=['PUT'])
def api_update_student(roll_number):
    data = request.get_json()
    student_name = data.get('student_name')
    section = data.get('section', '')
    phone_number = data.get('phone_number')
    email = data.get('email')
    college = data.get('college', '')
    address = data.get('address', '')
    
    if not all([student_name, email, phone_number]):
        return jsonify({'success': False, 'message': 'Please fill in all required fields'}), 400
    
    try:
        phone_number = int(phone_number)
    except ValueError:
        return jsonify({'success': False, 'message': 'Phone number must be a valid number'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if student exists
    cursor.execute('SELECT * FROM student WHERE roll_number = ?', (roll_number,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': 'Student not found'}), 404
    
    cursor.execute('''
        UPDATE student 
        SET student_name = ?, section = ?, email = ?, address = ?, phone_number = ?, college = ?
        WHERE roll_number = ?
    ''', (student_name, section, email, address, phone_number, college, roll_number))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Student updated successfully!'}), 200

@app.route('/api/students/<roll_number>', methods=['DELETE'])
def api_delete_student(roll_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if student exists
    cursor.execute('SELECT * FROM student WHERE roll_number = ?', (roll_number,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': 'Student not found'}), 404
    
    cursor.execute('DELETE FROM student WHERE roll_number = ?', (roll_number,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Student deleted successfully!'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
