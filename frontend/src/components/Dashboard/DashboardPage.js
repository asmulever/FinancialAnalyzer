import React from 'react';

function DashboardPage() {
  const styles = {
    dashboardContainer: {
      display: 'flex',
      height: '100vh', // Full viewport height
    },
    navMenu: {
      width: '200px', // Fixed width for nav
      backgroundColor: '#f0f0f0', // Light grey background
      padding: '20px',
      borderRight: '1px solid #ccc',
    },
    contentArea: {
      flexGrow: 1, // Takes remaining space
      padding: '20px',
      backgroundColor: '#fff', // White background
    },
  };

  return (
    <div style={styles.dashboardContainer}>
      <div style={styles.navMenu}>
        <p>Navigation Menu Placeholder</p>
        {/* Add navigation links here later */}
      </div>
      <div style={styles.contentArea}>
        <h1>Dashboard</h1>
        <p>Main Content Area Placeholder</p>
        {/* Add dashboard widgets and content here later */}
      </div>
    </div>
  );
}

export default DashboardPage;
