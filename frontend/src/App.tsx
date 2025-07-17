import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Container, Typography, Box } from '@mui/material';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom>
            GenAI Data Insights Platform
          </Typography>
          <Typography variant="h6" component="h2" gutterBottom>
            AI-powered business intelligence for retail analytics
          </Typography>
          <Typography variant="body1">
            Welcome to the platform. Natural language query interface coming soon.
          </Typography>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App; 