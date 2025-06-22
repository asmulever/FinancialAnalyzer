import React, { useState } from 'react';
import {
  Container,
  Box,
  TextField,
  Button,
  Typography,
  Link,
  Paper,
  Grid,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

// Asegúrate de que esta función onLogin se pase como prop desde App.jsx
function Login({ onLogin }) {
  const [isCreatingAccount, setIsCreatingAccount] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    console.log('Login attempt with:', { email, password });
    // Aquí iría la lógica de autenticación real.
    // Por ahora, simulamos un login exitoso si hay email y password.
    if (email && password) {
      if (typeof onLogin === 'function') {
        onLogin(); // Llama a onLogin para actualizar el estado de autenticación en App.jsx
      } else {
        console.error("onLogin prop is not a function or not provided");
      }
      navigate('/dashboard');
    } else {
      alert('Por favor, ingresa email y contraseña.');
    }
  };

  const handleCreateAccount = (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert("Las contraseñas no coinciden.");
      return;
    }
    console.log('Create account attempt with:', { email, password });
    // Aquí iría la lógica de creación de cuenta real.
    // Por ahora, simulamos creación y login exitosos.
    if (email && password) {
      if (typeof onLogin === 'function') {
        onLogin(); // Llama a onLogin para actualizar el estado de autenticación
      } else {
        console.error("onLogin prop is not a function or not provided");
      }
      navigate('/dashboard');
    } else {
      alert('Por favor, ingresa email y contraseña.');
    }
  };

  const toggleForm = () => {
    setIsCreatingAccount(!isCreatingAccount);
    setEmail('');
    setPassword('');
    setConfirmPassword('');
  };

  return (
    <Container component="main" maxWidth="xs">
      <Paper
        elevation={3}
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          padding: { xs: 2, sm: 3, md: 4 }, // Padding responsivo
        }}
      >
        <Typography component="h1" variant="h5" sx={{ mb: 2 }}>
          {isCreatingAccount ? 'Crear Cuenta' : 'Iniciar Sesión'}
        </Typography>
        <Box
          component="form"
          onSubmit={isCreatingAccount ? handleCreateAccount : handleLogin}
          noValidate
          sx={{ mt: 1, width: '100%' }}
        >
          <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label="Correo Electrónico"
            name="email"
            autoComplete="email"
            autoFocus
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Contraseña"
            type="password"
            id="password"
            autoComplete={isCreatingAccount ? 'new-password' : 'current-password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {isCreatingAccount && (
            <TextField
              margin="normal"
              required
              fullWidth
              name="confirmPassword"
              label="Confirmar Contraseña"
              type="password"
              id="confirmPassword"
              autoComplete="new-password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
          )}
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            {isCreatingAccount ? 'Crear Cuenta' : 'Iniciar Sesión'}
          </Button>
          <Grid container justifyContent="flex-end">
            <Grid item>
              <Link component="button" variant="body2" onClick={toggleForm} type="button">
                {isCreatingAccount
                  ? '¿Ya tienes una cuenta? Inicia sesión'
                  : '¿No tienes una cuenta? Crea una'}
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Paper>
    </Container>
  );
}

export default Login;
