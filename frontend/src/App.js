import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './components/Auth/LoginPage';
import DashboardPage from './components/Dashboard/DashboardPage'; // Import DashboardPage

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/" element={<LoginPage />} /> {/* Default to LoginPage for now */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
