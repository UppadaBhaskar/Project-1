import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import axios from 'axios';
import Login from './components/Login';
import Register from './components/Register';
import Home from './components/Home';
import StudentProfile from './components/StudentProfile';
import CreateStudent from './components/CreateStudent';
import UpdateStudent from './components/UpdateStudent';
import './App.css';

axios.defaults.withCredentials = true;

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const hasCheckedAuth = useRef(false);

  useEffect(() => {
    if (!hasCheckedAuth.current) {
      hasCheckedAuth.current = true;
      checkAuth();
    }
  }, []);

  const checkAuth = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/check-auth');
      setIsAuthenticated(response.data.authenticated);
    } catch (error) {
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = async () => {
    try {
      await axios.post('http://localhost:5000/api/logout');
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Router>
      <Routes>
        <Route 
          path="/login" 
          element={!isAuthenticated ? <Login onLogin={handleLogin} /> : <Navigate to="/" />} 
        />
        <Route 
          path="/register" 
          element={!isAuthenticated ? <Register /> : <Navigate to="/" />} 
        />
        <Route 
          path="/" 
          element={isAuthenticated ? <Home onLogout={handleLogout} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/student/:rollNumber" 
          element={isAuthenticated ? <StudentProfile /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/create-student" 
          element={isAuthenticated ? <CreateStudent /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/update-student/:rollNumber" 
          element={isAuthenticated ? <UpdateStudent /> : <Navigate to="/login" />} 
        />
      </Routes>
    </Router>
  );
}

export default App;

