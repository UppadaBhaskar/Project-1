import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './UpdateStudent.css';

function UpdateStudent() {
  const { rollNumber } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    student_name: '',
    section: '',
    phone_number: '',
    email: '',
    college: '',
    address: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
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
      const student = response.data;
      setFormData({
        student_name: student.student_name || '',
        section: student.section || '',
        phone_number: student.phone_number || '',
        email: student.email || '',
        college: student.college || '',
        address: student.address || ''
      });
    } catch (error) {
      console.error('Error fetching student:', error);
      setError('Failed to load student data');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await axios.put(`http://localhost:5000/api/students/${rollNumber}`, {
        ...formData,
        phone_number: parseInt(formData.phone_number)
      });
      if (response.status === 200) {
        navigate(`/student/${rollNumber}`);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update student');
    }
  };

  const handleCancel = () => {
    navigate(`/student/${rollNumber}`);
  };

  if (loading) {
    return <div className="update-student-container">Loading...</div>;
  }

  return (
    <div className="update-student-container">
      <div className="form-wrapper">
        <h2>Update Student Data</h2>
        <div className="form-box">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="roll_number">Roll number :</label>
              <input
                type="text"
                id="roll_number"
                name="roll_number"
                value={rollNumber}
                disabled
                className="disabled-input"
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
            <div className="button-group">
              <button type="button" className="cancel-button" onClick={handleCancel}>Cancel</button>
              <button type="submit" className="update-student-button">Update Student</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default UpdateStudent;

