# API Reference - College Management System

**Base URL:** `http://localhost:5000`

---

## 1. Register Faculty

**Endpoint:** `POST /api/register`

**Authentication:** Not Required

**Request Headers:**
```
Content-Type: application/json
```

**Request Payload:**
```json
{
  "faculty_name": "john_doe",
  "password": "password123"
}
```

**Success Response (201):**
```json
{
  "message": "Registration successful"
}
```

**Error Response (400) - Missing Fields:**
```json
{
  "error": "Faculty name and password are required"
}
```

**Error Response (400) - Faculty Exists:**
```json
{
  "error": "Faculty name already exists"
}
```

---

## 2. Login Faculty

**Endpoint:** `POST /api/login`

**Authentication:** Not Required

**Request Headers:**
```
Content-Type: application/json
```

**Request Payload:**
```json
{
  "faculty_name": "abc",
  "password": "abc123"
}
```

**Success Response (200):**
```json
{
  "message": "Login successful",
  "faculty_name": "abc"
}
```

**Error Response (400) - Missing Fields:**
```json
{
  "error": "Faculty name and password are required"
}
```

**Error Response (401) - Invalid Credentials:**
```json
{
  "error": "Invalid credentials"
}
```

---

## 3. Logout Faculty

**Endpoint:** `POST /api/logout`

**Authentication:** Required (Session)

**Request Headers:** None (session cookie sent automatically)

**Request Payload:** None

**Success Response (200):**
```json
{
  "message": "Logout successful"
}
```

---

## 4. Check Authentication Status

**Endpoint:** `GET /api/check-auth`

**Authentication:** Not Required (but returns auth status)

**Request Headers:** None

**Request Payload:** None

**Success Response (200) - Authenticated:**
```json
{
  "authenticated": true,
  "faculty_name": "abc"
}
```

**Success Response (401) - Not Authenticated:**
```json
{
  "authenticated": false
}
```

---

## 5. Get All Students

**Endpoint:** `GET /api/students`

**Authentication:** Required (Session)

**Request Headers:** None (session cookie sent automatically)

**Request Payload:** None

**Success Response (200):**
```json
[
  {
    "roll_number": "AB23",
    "student_name": "Manu",
    "section": "A"
  },
  {
    "roll_number": "CD45",
    "student_name": "Rahul K",
    "section": "D"
  }
]
```

**Empty Response (200):**
```json
[]
```

**Error Response (401) - Unauthorized:**
```json
{
  "error": "Unauthorized"
}
```

---

## 6. Create Student

**Endpoint:** `POST /api/students`

**Authentication:** Required (Session)

**Request Headers:**
```
Content-Type: application/json
```

**Request Payload:**
```json
{
  "roll_number": "20HP1A1232",
  "student_name": "Rahul K",
  "section": "D",
  "email": "rahulk@gmail.com",
  "address": "Bengaluru",
  "phone_number": 1234567890,
  "college": "ABC College"
}
```

**Field Details:**
- `roll_number` (string, required, max 10 chars, unique)
- `student_name` (string, required)
- `section` (string, optional, max 5 chars)
- `email` (string, required, valid email format)
- `address` (string, optional)
- `phone_number` (integer, required)
- `college` (string, optional)

**Success Response (201):**
```json
{
  "message": "Student created successfully"
}
```

**Error Response (400) - Missing Required Fields:**
```json
{
  "error": "Missing required fields"
}
```

**Error Response (400) - Roll Number Exists:**
```json
{
  "error": "Roll number already exists"
}
```

**Error Response (401) - Unauthorized:**
```json
{
  "error": "Unauthorized"
}
```

---

## 7. Get Student by Roll Number

**Endpoint:** `GET /api/students/<roll_number>`

**Authentication:** Required (Session)

**Request Headers:** None (session cookie sent automatically)

**URL Parameters:**
- `roll_number` (string, required) - Student's roll number

**Request Payload:** None

**Example Request:**
```
GET /api/students/AB23
```

**Success Response (200):**
```json
{
  "roll_number": "AB23",
  "student_name": "Manu",
  "section": "A",
  "email": "manu@example.com",
  "address": "Banglore",
  "phone_number": 1234567890,
  "college": "ABC College"
}
```

**Error Response (401) - Unauthorized:**
```json
{
  "error": "Unauthorized"
}
```

**Error Response (404) - Not Found:**
```json
{
  "error": "Student not found"
}
```

---

## 8. Update Student

**Endpoint:** `PUT /api/students/<roll_number>`

**Authentication:** Required (Session)

**Request Headers:**
```
Content-Type: application/json
```

**URL Parameters:**
- `roll_number` (string, required) - Student's roll number (cannot be changed)

**Request Payload:**
```json
{
  "student_name": "Manu Updated",
  "section": "B",
  "email": "manu.updated@example.com",
  "address": "Mumbai",
  "phone_number": 9876543210,
  "college": "XYZ College"
}
```

**Field Details:**
- `student_name` (string, required)
- `section` (string, optional, max 5 chars)
- `email` (string, required, valid email format)
- `address` (string, optional)
- `phone_number` (integer, required)
- `college` (string, optional)
- **Note:** `roll_number` is NOT in payload (cannot be updated)

**Example Request:**
```
PUT /api/students/AB23
```

**Success Response (200):**
```json
{
  "message": "Student updated successfully"
}
```

**Error Response (400) - Missing Required Fields:**
```json
{
  "error": "Missing required fields"
}
```

**Error Response (401) - Unauthorized:**
```json
{
  "error": "Unauthorized"
}
```

**Error Response (404) - Not Found:**
```json
{
  "error": "Student not found"
}
```

---

## 9. Delete Student

**Endpoint:** `DELETE /api/students/<roll_number>`

**Authentication:** Required (Session)

**Request Headers:** None (session cookie sent automatically)

**URL Parameters:**
- `roll_number` (string, required) - Student's roll number

**Request Payload:** None

**Example Request:**
```
DELETE /api/students/AB23
```

**Success Response (200):**
```json
{
  "message": "Student deleted successfully"
}
```

**Error Response (401) - Unauthorized:**
```json
{
  "error": "Unauthorized"
}
```

**Error Response (404) - Not Found:**
```json
{
  "error": "Student not found"
}
```

---

## HTTP Status Codes Summary

| Status Code | Meaning |
|------------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request data or missing fields |
| 401 | Unauthorized - Authentication required or invalid |
| 404 | Not Found - Resource not found |

---

## Authentication Notes

- **Session-based authentication** using Flask sessions
- After successful login, session cookie is automatically sent with subsequent requests
- All student endpoints require authentication
- Use `withCredentials: true` in frontend requests to include cookies
- Session expires when browser is closed (by default)

---

## Quick Test Examples

### Using cURL

**1. Register:**
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"faculty_name": "test", "password": "test123"}'
```

**2. Login:**
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"faculty_name": "abc", "password": "abc123"}'
```

**3. Get Students (after login):**
```bash
curl -X GET http://localhost:5000/api/students -b cookies.txt
```

**4. Create Student (after login):**
```bash
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "roll_number": "STU001",
    "student_name": "John Doe",
    "section": "A",
    "email": "john@example.com",
    "address": "New York",
    "phone_number": 1234567890,
    "college": "ABC College"
  }'
```

**5. Get Student (after login):**
```bash
curl -X GET http://localhost:5000/api/students/AB23 -b cookies.txt
```

**6. Update Student (after login):**
```bash
curl -X PUT http://localhost:5000/api/students/AB23 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "student_name": "Updated Name",
    "section": "B",
    "email": "updated@example.com",
    "address": "Updated Address",
    "phone_number": 9876543210,
    "college": "XYZ College"
  }'
```

**7. Delete Student (after login):**
```bash
curl -X DELETE http://localhost:5000/api/students/AB23 -b cookies.txt
```

**8. Logout:**
```bash
curl -X POST http://localhost:5000/api/logout -b cookies.txt
```

---

## Using JavaScript/Fetch

**Example - Login:**
```javascript
fetch('http://localhost:5000/api/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include', // Important for cookies
  body: JSON.stringify({
    faculty_name: 'abc',
    password: 'abc123'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

**Example - Get Students:**
```javascript
fetch('http://localhost:5000/api/students', {
  method: 'GET',
  credentials: 'include' // Important for cookies
})
.then(response => response.json())
.then(data => console.log(data));
```

**Example - Create Student:**
```javascript
fetch('http://localhost:5000/api/students', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include',
  body: JSON.stringify({
    roll_number: 'STU001',
    student_name: 'John Doe',
    section: 'A',
    email: 'john@example.com',
    address: 'New York',
    phone_number: 1234567890,
    college: 'ABC College'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```


