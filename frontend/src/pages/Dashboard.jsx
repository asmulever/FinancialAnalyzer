import React from 'react';
import { Box, Container, Grid, Paper, Typography } from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import KpiCard from '../components/KpiCard'; // Ajusta la ruta si es necesario

// Iconos para las KPI cards (opcional, pero mejora la UI)
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';

// Datos de ejemplo para el gráfico
const monthlyData = [
  { name: 'Ene', saldo: 1200 },
  { name: 'Feb', saldo: 2100 },
  { name: 'Mar', saldo: 1800 },
  { name: 'Abr', saldo: 2400 },
  { name: 'May', saldo: 2200 },
  { name: 'Jun', saldo: 3000 },
  { name: 'Jul', saldo: 2800 },
  { name: 'Ago', saldo: 3500 },
  { name: 'Sep', saldo: 3200 },
  { name: 'Oct', saldo: 4000 },
  { name: 'Nov', saldo: 4500 },
  { name: 'Dic', saldo: 5000 },
];

// Datos de ejemplo para las KPIs
const kpiData = {
  ingresos: {
    value: '$15,250',
    icon: <AttachMoneyIcon fontSize="large" />,
    color: 'success.main',
  },
  egresos: {
    value: '$7,800',
    icon: <TrendingDownIcon fontSize="large" />,
    color: 'error.main',
  },
  balance: {
    value: '$7,450',
    icon: <AccountBalanceWalletIcon fontSize="large" />,
    color: 'primary.main',
  },
};

function Dashboard() {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold', mb: 3 }}>
        Análisis Financiero
      </Typography>

      {/* Sección de KPIs */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={4}>
          <KpiCard
            title="Ingresos Totales"
            value={kpiData.ingresos.value}
            icon={kpiData.ingresos.icon}
            color={kpiData.ingresos.color}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <KpiCard
            title="Egresos Totales"
            value={kpiData.egresos.value}
            icon={kpiData.egresos.icon}
            color={kpiData.egresos.color}
          />
        </Grid>
        <Grid item xs={12} sm={12} md={4}> {/* Full width on small, half on sm, third on md */}
          <KpiCard
            title="Balance Actual"
            value={kpiData.balance.value}
            icon={kpiData.balance.icon}
            color={kpiData.balance.color}
          />
        </Grid>
      </Grid>

      {/* Sección del Gráfico */}
      <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 400, boxShadow: 3 }}>
        <Typography variant="h6" component="h2" gutterBottom sx={{ fontWeight: 'medium' }}>
          Evolución del Saldo Mensual
        </Typography>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={monthlyData}
            margin={{
              top: 16,
              right: 16,
              bottom: 0,
              left: 24,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="saldo" stroke="#8884d8" strokeWidth={2} activeDot={{ r: 8 }} />
          </LineChart>
        </ResponsiveContainer>
      </Paper>
    </Container>
  );
}

export default Dashboard;
