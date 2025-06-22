import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';

function KpiCard({ title, value, icon, color = 'text.primary' }) {
  return (
    <Card sx={{ display: 'flex', flexDirection: 'column', height: '100%', boxShadow: 3 }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          {icon && React.cloneElement(icon, { sx: { mr: 1, color: color } })}
          <Typography sx={{ fontWeight: 'medium' }} color="text.secondary" gutterBottom>
            {title}
          </Typography>
        </Box>
        <Typography variant="h4" component="div" sx={{ fontWeight: 'bold', color: color }}>
          {value}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default KpiCard;
