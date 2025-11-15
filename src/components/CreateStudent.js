import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './CreateStudent.css';

function CreateStudent() {
  const [formData, setFormData] = useState({
    roll_number: '',
    student_name: '',
    section: '',
    phone_number: '',
    email: '',
    college: '',
    address: ''
  });
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setShowConfirmModal(true);
  };

  const handleConfirm = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/students', {
        ...formData,
        phone_number: parseInt(formData.phone_number)
      });
      if (response.status === 201) {
        navigate('/');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create student');
      setShowConfirmModal(false);
    }
  };

  const handleCancel = () => {
    setShowConfirmModal(false);
  };

  const handleCloseModal = () => {
    setShowConfirmModal(false);
  };

  return (
    <div className="create-student-container">
      <div className="form-wrapper">
        <h2>Create student</h2>
        <div className="form-box">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="roll_number">Roll number :</label>
              <input
                type="text"
                id="roll_number"
                name="roll_number"
                value={formData.roll_number}
                onChange={handleChange}
                maxLength={10}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="student_name">Student Name :</label>
              <input
                type="text"
                id="student_name"
                name="student_name"
                value={formData.student_name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="section">Section :</label>
              <input
                type="text"
                id="section"
                name="section"
                value={formData.section}
                onChange={handleChange}
                maxLength={5}
              />
            </div>
            <div className="form-group">
              <label htmlFor="phone_number">Phone number :</label>
              <input
                type="tel"
                id="phone_number"
                name="phone_number"
                value={formData.phone_number}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">email :</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="college">College :</label>
              <input
                type="text"
                id="college"
                name="college"
                value={formData.college}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="address">Address :</label>
              <input
                type="text"
                id="address"
                name="address"
                value={formData.address}
                onChange={handleChange}
              />
            </div>
            {error && <div className="error-message">{error}</div>}
            <button type="submit" className="create-student-button">Create Student</button>
          </form>
        </div>
      </div>

      {showConfirmModal && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Confirm Creation</h3>
              <button className="close-button" onClick={handleCloseModal}>×</button>
            </div>
            <div className="modal-body">
              <p>Are you sure to create a new student</p>
            </div>
            <div className="modal-footer">
              <button className="no-button" onClick={handleCancel}>No</button>
              <button className="yes-button" onClick={handleConfirm}>Yes</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default CreateStudent;


