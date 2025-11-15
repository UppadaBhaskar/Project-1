import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Home.css';

function Home({ onLogout }) {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const hasFetched = useRef(false);

  useEffect(() => {
    if (!hasFetched.current) {
      hasFetched.current = true;
      fetchStudents();
    }
  }, []);

  const fetchStudents = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/students');
      setStudents(response.data);
    } catch (error) {
      console.error('Error fetching students:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleViewProfile = (rollNumber) => {
    navigate(`/student/${rollNumber}`);
  };

  const handleCreateStudent = () => {
    navigate('/create-student');
  };

  const handleLogout = async () => {
    await onLogout();
    navigate('/login');
  };

  if (loading) {
    return <div className="home-container">Loading...</div>;
  }

  return (
    <div className="home-container">
      <div className="header">
        <h1>Student Data</h1>
        <div className="header-buttons">
          <button className="logout-button" onClick={handleLogout}>Logout</button>
          <button className="create-button" onClick={handleCreateStudent}>Create Student</button>
        </div>
      </div>
      <div className="table-container">
        <table className="students-table">
          <thead>
            <tr>
              <th>Roll number</th>
              <th>Student Name</th>
              <th>Section</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {students.length === 0 ? (
              <tr>
                <td colSpan="4" style={{ textAlign: 'center' }}>No students found</td>
              </tr>
            ) : (
              students.map((student) => (
                <tr key={student.roll_number}>
                  <td>{student.roll_number}</td>
                  <td>{student.student_name}</td>
                  <td>{student.section || 'N/A'}</td>
                  <td>
                    <button 
                      className="view-profile-button"
                      onClick={() => handleViewProfile(student.roll_number)}
                    >
                      View Profile
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Home;

