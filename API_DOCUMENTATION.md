# API Documentation

Base URL: `http://localhost:5000`

All API endpoints return JSON responses. Authentication is session-based using Flask sessions.

---

## Authentication Endpoints

### 1. Register Faculty

**Endpoint:** `POST /api/register`

**Description:** Register a new faculty member

**Authentication Required:** No

**Request Headers:**
```
Content-Type: application/json
```

**Request Payload:**
```json
{
  "faculty_name": "string (required)",
  "password": "string (required, max 12 characters)"
}
```

**Example Request:**
```json
{
  "faculty_name": "john_doe",
  "password": "password123"
}
```

**Success Response (201 Created):**
```json
{
  "message": "Registration successful"
}
```

**Error Responses:**

**400 Bad Request - Missing Fields:**
```json
{
  "error": "Faculty name and password are required"
}
```

**400 Bad Request - Faculty Already Exists:**
```json
{
  "error": "Faculty name already exists"
}
```

---

### 2. Login Faculty

**Endpoint:** `POST /api/login`

**Description:** Authenticate faculty member and create session

**Authentication Required:** No

**Request Headers:**
```
Content-Type: application/json
```

**Request Payload:**
```json
{
  "faculty_name": "string (required)",
  "password": "string (required)"
}
```

**Example Request:**
```json
{
  "faculty_name": "abc",
  "password": "abc123"
}
```

**Success Response (200 OK):**
```json
{
  "message": "Login successful",
  "faculty_name": "abc"
}
```

**Error Responses:**

**400 Bad Request - Missing Fields:**
```json
{
  "error": "Faculty name and password are required"
}
```

**401 Unauthorized - Invalid Credentials:**
```json
{
  "error": "Invalid credentials"
}
```

---

### 3. Logout Faculty

**Endpoint:** `POST /api/logout`

**Description:** Logout current faculty member and clear session

**Authentication Required:** Yes (Session)

**Request Headers:**
```
Content-Type: application/json
```

**Request Payload:** None

**Success Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

---

### 4. Check Authentication Status

**Endpoint:** `GET /api/check-auth`

**Description:** Check if user is authenticated and get faculty name

**Authentication Required:** No (but returns authenticated status)

**Request Headers:** None

**Request Payload:** None

**Success Response (200 OK) - Authenticated:**
```json
{
  "authenticated": true,
  "faculty_name": "abc"
}
```

**Success Response (401 Unauthorized) - Not Authenticated:**
```json
{
  "authenticated": false
}
```

---

## Student Endpoints

### 5. Get All Students

**Endpoint:** `GET /api/students`

**Description:** Retrieve list of all students (limited fields for listing)

**Authentication Required:** Yes (Session)

**Request Headers:** None (session cookie sent automatically)

**Request Payload:** None

**Success Response (200 OK):**
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

**Empty Response (200 OK):**
```json
[]
```

**Error Response (401 Unauthorized):**
```json
{
  "error": "Unauthorized"
}
```

---

### 6. Create Student

**Endpoint:** `POST /api/students`

**Description:** Create a new student record

**Authentication Required:** Yes (Session)

**Request Headers:**
```
Content-Type: application/json
```

**Request Payload:**
```json
{
  "roll_number": "string (required, max 10 characters, unique)",
  "student_name": "string (required)",
  "section": "string (optional, max 5 characters)",
  "email": "string (required, valid email format)",
  "address": "string (optional)",
  "phone_number": "integer (required)",
  "college": "string (optional)"
}
```

**Example Request:**
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

**Success Response (201 Created):**
```json
{
  "message": "Student created successfully"
}
```

**Error Responses:**

**400 Bad Request - Missing Required Fields:**
```json
{
  "error": "Missing required fields"
}
```

**400 Bad Request - Roll Number Already Exists:**
```json
{
  "error": "Roll number already exists"
}
```

**401 Unauthorized:**
```json
{
  "error": "Unauthorized"
}
```

---

### 7. Get Student by Roll Number

**Endpoint:** `GET /api/students/<roll_number>`

**Description:** Retrieve complete details of a specific student

**Authentication Required:** Yes (Session)

**Request Headers:** None (session cookie sent automatically)

**URL Parameters:**
- `roll_number` (string, required): Student's roll number

**Request Payload:** None

**Example Request:**
```
GET /api/students/AB23
```

**Success Response (200 OK):**
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

**Error Responses:**

**401 Unauthorized:**
```json
{
  "error": "Unauthorized"
}
```

**404 Not Found:**
```json
{
  "error": "Student not found"
}
```

---

### 8. Update Student

**Endpoint:** `PUT /api/students/<roll_number>`

**Description:** Update student information (roll number cannot be changed)

**Authentication Required:** Yes (Session)

**Request Headers:**
```
Content-Type: application/json
```

**URL Parameters:**
- `roll_number` (string, required): Student's roll number (cannot be changed)

**Request Payload:**
```json
{
  "student_name": "string (required)",
  "section": "string (optional, max 5 characters)",
  "email": "string (required, valid email format)",
  "address": "string (optional)",
  "phone_number": "integer (required)",
  "college": "string (optional)"
}
```

**Note:** `roll_number` is NOT included in the payload as it cannot be updated.

**Example Request:**
```
PUT /api/students/AB23
```

**Example Payload:**
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

**Success Response (200 OK):**
```json
{
  "message": "Student updated successfully"
}
```

**Error Responses:**

**400 Bad Request - Missing Required Fields:**
```json
{
  "error": "Missing required fields"
}
```

**401 Unauthorized:**
```json
{
  "error": "Unauthorized"
}
```

**404 Not Found:**
```json
{
  "error": "Student not found"
}
```

---

### 9. Delete Student

**Endpoint:** `DELETE /api/students/<roll_number>`

**Description:** Delete a student record

**Authentication Required:** Yes (Session)

**Request Headers:** None (session cookie sent automatically)

**URL Parameters:**
- `roll_number` (string, required): Student's roll number

**Request Payload:** None

**Example Request:**
```
DELETE /api/students/AB23
```

**Success Response (200 OK):**
```json
{
  "message": "Student deleted successfully"
}
```

**Error Responses:**

**401 Unauthorized:**
```json
{
  "error": "Unauthorized"
}
```

**404 Not Found:**
```json
{
  "error": "Student not found"
}
```

---

## HTTP Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data or missing required fields
- **401 Unauthorized**: Authentication required or invalid credentials
- **404 Not Found**: Resource not found

---

## Session Management

- Sessions are managed using Flask sessions (cookies)
- Session cookie is automatically sent with requests after login
- Session contains `faculty_id` and `faculty_name`
- Session expires when browser is closed (by default)
- Use `withCredentials: true` in frontend requests to include cookies

---

## Example cURL Commands

### Register
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"faculty_name": "test_user", "password": "test123"}'
```

### Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"faculty_name": "abc", "password": "abc123"}'
```

### Get All Students (after login)
```bash
curl -X GET http://localhost:5000/api/students \
  -b cookies.txt
```

### Create Student (after login)
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

### Get Student (after login)
```bash
curl -X GET http://localhost:5000/api/students/AB23 \
  -b cookies.txt
```

### Update Student (after login)
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

### Delete Student (after login)
```bash
curl -X DELETE http://localhost:5000/api/students/AB23 \
  -b cookies.txt
```

### Logout
```bash
curl -X POST http://localhost:5000/api/logout \
  -b cookies.txt
```

---

## Data Types

- **String**: Text data
- **Integer**: Numeric data (for phone_number)
- **VARCHAR**: Variable-length string (database type)
- **Boolean**: true/false (for authenticated status)

---

## Field Constraints

### Faculty
- `faculty_name`: Required, unique, VARCHAR
- `password`: Required, max 12 characters, stored as hash

### Student
- `roll_number`: Required, VARCHAR(10), PRIMARY KEY, unique, cannot be updated
- `student_name`: Required, VARCHAR
- `section`: Optional, VARCHAR(5)
- `email`: Required, VARCHAR, should be valid email format
- `address`: Optional, VARCHAR
- `phone_number`: Required, INTEGER
- `college`: Optional, VARCHAR




