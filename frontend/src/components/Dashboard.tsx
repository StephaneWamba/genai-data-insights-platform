import React, { useState } from 'react';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  useTheme,
  useMediaQuery,
  Chip,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  QueryStats as QueryIcon,
  Analytics as AnalyticsIcon,
  People as PeopleIcon,
  Inventory as InventoryIcon,
  TrendingUp as TrendingIcon,
  Lightbulb as InsightsIcon,
} from '@mui/icons-material';
import QueryInterface from './QueryInterface';
import DataVisualization from './DataVisualization';
import BusinessMetrics from './BusinessMetrics';
import QueryHistory from './QueryHistory';

// Navigation items
const navigationItems = [
  { id: 'dashboard', label: 'Dashboard', icon: <DashboardIcon /> },
  { id: 'query', label: 'Natural Language Query', icon: <QueryIcon /> },
  { id: 'analytics', label: 'Data Analytics', icon: <AnalyticsIcon /> },
  { id: 'customers', label: 'Customer Insights', icon: <PeopleIcon /> },
  { id: 'inventory', label: 'Inventory Status', icon: <InventoryIcon /> },
  { id: 'trends', label: 'Sales Trends', icon: <TrendingIcon /> },
  { id: 'insights', label: 'AI Insights', icon: <InsightsIcon /> },
];

const drawerWidth = 280;

export default function Dashboard() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [mobileOpen, setMobileOpen] = useState(false);
  const [activeSection, setActiveSection] = useState('dashboard');

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleNavigation = (sectionId: string) => {
    setActiveSection(sectionId);
    if (isMobile) {
      setMobileOpen(false);
    }
  };

  // Render content based on active section
  const renderContent = () => {
    switch (activeSection) {
      case 'dashboard':
        return <BusinessMetrics />;
      case 'query':
        return <QueryInterface />;
      case 'analytics':
        return <DataVisualization />;
      case 'customers':
        return <DataVisualization dataType="customers" />;
      case 'inventory':
        return <DataVisualization dataType="inventory" />;
      case 'trends':
        return <DataVisualization dataType="sales" />;
      case 'insights':
        return <QueryHistory />;
      default:
        return <BusinessMetrics />;
    }
  };

  // Drawer content
  const drawer = (
    <Box>
      <Toolbar>
        <Typography variant="h6" noWrap component="div" sx={{ fontWeight: 600 }}>
          GenAI Insights
        </Typography>
      </Toolbar>
      <Box sx={{ px: 2, py: 1 }}>
        <Chip 
          label="AI-Powered Analytics" 
          color="primary" 
          size="small" 
          variant="outlined"
        />
      </Box>
      <List sx={{ mt: 2 }}>
        {navigationItems.map((item) => (
          <ListItem key={item.id} disablePadding>
            <ListItemButton
              selected={activeSection === item.id}
              onClick={() => handleNavigation(item.id)}
              sx={{
                mx: 1,
                borderRadius: 2,
                '&.Mui-selected': {
                  backgroundColor: 'primary.main',
                  color: 'primary.contrastText',
                  '&:hover': {
                    backgroundColor: 'primary.dark',
                  },
                  '& .MuiListItemIcon-root': {
                    color: 'primary.contrastText',
                  },
                },
              }}
            >
              <ListItemIcon
                sx={{
                  minWidth: 40,
                  color: activeSection === item.id ? 'primary.contrastText' : 'inherit',
                }}
              >
                {item.icon}
              </ListItemIcon>
              <ListItemText 
                primary={item.label}
                primaryTypographyProps={{
                  fontSize: '0.9rem',
                  fontWeight: activeSection === item.id ? 600 : 400,
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      {/* App Bar */}
      <AppBar
        position="fixed"
        sx={{
          width: { md: `calc(100% - ${drawerWidth}px)` },
          ml: { md: `${drawerWidth}px` },
          backgroundColor: 'white',
          color: 'text.primary',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { md: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            {navigationItems.find(item => item.id === activeSection)?.label || 'Dashboard'}
          </Typography>
          <Chip 
            label="Live Data" 
            color="success" 
            size="small" 
            variant="outlined"
          />
        </Toolbar>
      </AppBar>

      {/* Navigation Drawer */}
      <Box
        component="nav"
        sx={{ width: { md: drawerWidth }, flexShrink: { md: 0 } }}
      >
        {/* Mobile drawer */}
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: { xs: 'block', md: 'none' },
            '& .MuiDrawer-paper': { 
              boxSizing: 'border-box', 
              width: drawerWidth,
              backgroundColor: 'background.paper',
            },
          }}
        >
          {drawer}
        </Drawer>
        
        {/* Desktop drawer */}
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', md: 'block' },
            '& .MuiDrawer-paper': { 
              boxSizing: 'border-box', 
              width: drawerWidth,
              backgroundColor: 'background.paper',
              borderRight: '1px solid',
              borderColor: 'divider',
            },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { md: `calc(100% - ${drawerWidth}px)` },
          mt: '64px', // AppBar height
        }}
      >
        {renderContent()}
      </Box>
    </Box>
  );
} 