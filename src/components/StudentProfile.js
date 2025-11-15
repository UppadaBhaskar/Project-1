import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './StudentProfile.css';

function StudentProfile() {
  const { rollNumber } = useParams();
  const navigate = useNavigate();
  const [student, setStudent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const lastRollNumber = useRef(null);

  useEffect(() => {
    if (lastRollNumber.current !== rollNumber) {
      lastRollNumber.current = rollNumber;
      fetchStudent();
    }
  }, [rollNumber]);

  const fetchStudent = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:5000/api/students/${rollNumber}`);
      setStudent(response.data);
    } catch (error) {
      console.error('Error fetching student:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = () => {
    navigate(`/update-student/${rollNumber}`);
  };

  const handleDelete = async () => {
    try {
      await axios.delete(`http://localhost:5000/api/students/${rollNumber}`);
      navigate('/');
    } catch (error) {
      console.error('Error deleting student:', error);
      alert('Failed to delete student');
    }
  };

  const handleBack = () => {
    navigate('/');
  };

  if (loading) {
    return <div className="profile-container">Loading...</div>;
  }

  if (!student) {
    return <div className="profile-container">Student not found</div>;
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h1>Student Data</h1>
        <button className="back-button" onClick={handleBack}>Back to List</button>
      </div>
      <div className="profile-card">
        <div className="profile-actions">
          <button className="edit-button" onClick={handleEdit}>Edit</button>
        </div>
        <div className="profile-info">
          <div className="info-row">
            <span className="info-label">Roll number :</span>
            <span className="info-value">{student.roll_number}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Student Name :</span>
            <span className="info-value">{student.student_name}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Section :</span>
            <span className="info-value">{student.section || 'N/A'}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Phone number :</span>
            <span className="info-value">{student.phone_number}</span>
          </div>
          <div className="info-row">
            <span className="info-label">email :</span>
            <span className="info-value">{student.email}</span>
          </div>
          <div className="info-row">
            <span className="info-label">College :</span>
            <span className="info-value">{student.college || 'N/A'}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Address :</span>
            <span className="info-value">{student.address || 'N/A'}</span>
          </div>
        </div>
        <div className="delete-container">
          <button className="delete-button" onClick={() => setShowDeleteConfirm(true)}>
            🗑️
          </button>
        </div>
      </div>

      {showDeleteConfirm && (
        <div className="modal-overlay" onClick={() => setShowDeleteConfirm(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Confirm Deletion</h3>
              <button className="close-button" onClick={() => setShowDeleteConfirm(false)}>×</button>
            </div>
            <div className="modal-body">
              <p>Are you sure you want to delete this student?</p>
            </div>
            <div className="modal-footer">
              <button className="no-button" onClick={() => setShowDeleteConfirm(false)}>No</button>
              <button className="yes-button" onClick={handleDelete}>Yes</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default StudentProfile;

