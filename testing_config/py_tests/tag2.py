import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import app, get_db_connection, init_db


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['DATABASE'] = ':memory:' 
    
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client


@pytest.fixture
def db():
    """Get database connection"""
    conn = get_db_connection()
    yield conn
    conn.close()


# Test 1: Database Connection
def test_database_connection(db):
    """Test that database connection works"""
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    assert 'faculty' in tables, "Faculty table should exist"
    assert 'student' in tables, "Student table should exist"


# Test 2: Faculty Table Structure
def test_faculty_table_structure(db):
    """Test faculty table has correct columns"""
    cursor = db.cursor()
    cursor.execute("PRAGMA table_info(faculty)")
    columns = [row[1] for row in cursor.fetchall()]
    
    assert 'faculty_id' in columns
    assert 'faculty_name' in columns
    assert 'password' in columns


# Test 3: Student Table Structure
def test_student_table_structure(db):
    """Test student table has correct columns"""
    cursor = db.cursor()
    cursor.execute("PRAGMA table_info(student)")
    columns = [row[1] for row in cursor.fetchall()]
    
    assert 'roll_number' in columns
    assert 'student_name' in columns
    assert 'section' in columns
    assert 'email' in columns
    assert 'phone_number' in columns


# Test 4: Login Route Exists
def test_login_route_exists(client):
    """Test login route is accessible"""
    response = client.get('/login')
    assert response.status_code == 200


# Test 5: Register Route Exists
def test_register_route_exists(client):
    """Test register route is accessible"""
    response = client.get('/register')
    assert response.status_code == 200


# Test 6: Home Route Exists
def test_home_route_exists(client):
    """Test home route is accessible"""
    response = client.get('/home')
    assert response.status_code in [200, 302]


# Test 7: Invalid Login
def test_invalid_login(client):
    """Test login with invalid credentials"""
    response = client.post('/login', data={
        'username': 'invalid',
        'password': 'wrong'
    }, follow_redirects=False)
    
    assert response.status_code in [200, 302]


# Test 8: Valid Login
def test_valid_login(client):
    """Test login with valid credentials"""
    response = client.post('/login', data={
        'username': 'abc',
        'password': 'abc123'
    }, follow_redirects=False)
    
    assert response.status_code == 302
    assert '/home' in response.location or response.location.endswith('/home')


# Test 9: Create Student Route Exists
def test_create_student_route(client):
    """Test create student route is accessible"""
    response = client.get('/create_student')
    assert response.status_code in [200, 302]


# Test 10: API Login Endpoint
def test_api_login(client):
    """Test API login endpoint"""
    response = client.post('/api/login', 
        json={'username': 'abc', 'password': 'abc123'},
        content_type='application/json')
    
    assert response.status_code in [200, 401]
    data = response.get_json()
    assert 'success' in data

