import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Login.css';

function Login({ onLogin }) {
  const [formData, setFormData] = useState({
    faculty_name: '',
    password: ''
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

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
      const response = await axios.post('http://localhost:5000/api/login', formData);
      if (response.status === 200) {
        onLogin();
        navigate('/');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed');
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Faculty Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="faculty_name">Username</label>
            <input
              type="text"
              id="faculty_name"
              name="faculty_name"
              value={formData.faculty_name}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          {error && <div className="error-message">{error}</div>}
          <div className="link-container">
            <Link to="/register">Create a new account</Link>
          </div>
          <button type="submit" className="signin-button">Sign in</button>
        </form>
      </div>
    </div>
  );
}

export default Login;


