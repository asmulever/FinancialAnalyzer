import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css'; // Estilos globales
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';

// Un tema básico de Material UI (opcional, puedes personalizarlo)
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2', // Un azul estándar
    },
    secondary: {
      main: '#dc004e', // Un rosa estándar
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  }
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <CssBaseline /> {/* Normaliza estilos y aplica el fondo del tema */}
        <App />
      </ThemeProvider>
    </BrowserRouter>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// import reportWebVitals from './reportWebVitals'; // Descomenta si lo necesitas
// reportWebVitals();
