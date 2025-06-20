import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate(); // Initialize navigate

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');

    try {
      const response = await axios.post('http://localhost:5000/auth/login', {
        username: username,
        password: password,
      });

      if (response.status === 200 && response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        console.log('Login successful! Token:', response.data.access_token);
        navigate('/dashboard'); // Redirect to dashboard
      } else {
        setError('Login failed. Invalid response from server.');
        console.error('Login failed: Invalid response', response);
      }
    } catch (err) {
      console.error('Login error:', err);
      if (err.response && err.response.data && err.response.data.message) {
        setError(err.response.data.message);
      } else if (err.request) {
        setError('Login failed. No response from server.');
      } else {
        setError('Login failed. An unexpected error occurred.');
      }
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <div>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default LoginPage;
