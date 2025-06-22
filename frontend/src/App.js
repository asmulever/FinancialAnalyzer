import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import Login from './pages/Login'; // Ajusta la ruta si es necesario
import Dashboard from './pages/Dashboard'; // Ajusta la ruta si es necesario
import { Box } from '@mui/material'; // Box se usará como contenedor principal

// Componente para rutas protegidas
function ProtectedRoute({ isAuthenticated, children }) {
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

function App() {
  // Intenta cargar el estado de autenticación desde localStorage
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    const savedAuthState = localStorage.getItem('isAuthenticated');
    return savedAuthState ? JSON.parse(savedAuthState) : false;
  });
  const navigate = useNavigate();

  // Guarda el estado de autenticación en localStorage cuando cambie
  useEffect(() => {
    localStorage.setItem('isAuthenticated', JSON.stringify(isAuthenticated));
  }, [isAuthenticated]);

  const handleLogin = () => {
    setIsAuthenticated(true);
    // No es necesario navigate aquí si Login.jsx ya lo hace.
    // Pero si quisiéramos forzarlo desde App: navigate('/dashboard');
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    navigate('/login'); // Redirige a login al cerrar sesión
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* Podrías tener una Navbar aquí si isAuthenticated es true */}
      {/* Ejemplo simple de Navbar condicional:
      {isAuthenticated && (
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Mi App Financiera
            </Typography>
            <Button color="inherit" onClick={handleLogout}>Cerrar Sesión</Button>
          </Toolbar>
        </AppBar>
      )}
      */}
      <Box component="main" sx={{ flexGrow: 1 /* p: 3 // Opcional: padding global */ }}>
        <Routes>
          <Route
            path="/login"
            element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login onLogin={handleLogin} />}
          />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute isAuthenticated={isAuthenticated}>
                <Dashboard />
                {/* Aquí podrías añadir un botón de logout visible en el dashboard */}
                {/* <Button variant="contained" onClick={handleLogout} sx={{mt: 2}}>Cerrar Sesión</Button> */}
              </ProtectedRoute>
            }
          />
          {/* Redirige cualquier otra ruta a login si no está autenticado, o a dashboard si sí lo está */}
          <Route
            path="*"
            element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />}
          />
        </Routes>
      </Box>
    </Box>
  );
}

export default App;
