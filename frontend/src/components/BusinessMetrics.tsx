import React, { useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  CircularProgress,
  Alert,
  Chip,
  Divider,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  AttachMoney as RevenueIcon,
  AccountBalance as ProfitIcon,
  People as CustomerIcon,
  ShoppingCart as OrderIcon,
  Inventory as InventoryIcon,
  Speed as SpeedIcon,
} from '@mui/icons-material';
import { useData } from '../contexts/DataContext';
import { dataAPI } from '../services/api';

export default function BusinessMetrics() {
  const { state, dispatch } = useData();

  useEffect(() => {
    const fetchMetrics = async () => {
      dispatch({ type: 'SET_LOADING', payload: true });
      try {
        const metrics = await dataAPI.getBusinessMetrics();
        dispatch({ type: 'SET_METRICS', payload: metrics });
      } catch (error: any) {
        const errorMessage = error.response?.data?.message || 'Failed to load business metrics';
        dispatch({ type: 'SET_ERROR', payload: errorMessage });
      } finally {
        dispatch({ type: 'SET_LOADING', payload: false });
      }
    };

    fetchMetrics();
  }, [dispatch]);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US').format(num);
  };

  const formatPercentage = (value: number) => {
    return `${value.toFixed(1)}%`;
  };

  const getMetricIcon = (metricType: string) => {
    switch (metricType) {
      case 'revenue':
        return <RevenueIcon />;
      case 'profit':
        return <ProfitIcon />;
      case 'customers':
        return <CustomerIcon />;
      case 'order':
        return <OrderIcon />;
      case 'inventory':
        return <InventoryIcon />;
      case 'speed':
        return <SpeedIcon />;
      default:
        return <TrendingUpIcon />;
    }
  };

  const getMetricColor = (metricType: string, value: number) => {
    switch (metricType) {
      case 'revenue':
      case 'profit':
      case 'customers':
        return 'success';
      case 'margin':
        return value > 20 ? 'success' : value > 10 ? 'warning' : 'error';
      case 'turnover':
        return value > 4 ? 'success' : value > 2 ? 'warning' : 'error';
      default:
        return 'primary';
    }
  };

  if (state.isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (state.error) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        {state.error}
      </Alert>
    );
  }

  if (!state.metrics) {
    return (
      <Alert severity="info">
        No metrics data available. Please try again later.
      </Alert>
    );
  }

  const metrics = state.metrics;

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
          Business Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Real-time business metrics and performance indicators
        </Typography>
      </Box>

      {/* Key Metrics Grid */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Total Revenue */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <RevenueIcon color="success" sx={{ mr: 1 }} />
                <Typography variant="h6" color="text.secondary">
                  Total Revenue
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
                {formatCurrency(metrics.total_revenue)}
              </Typography>
              <Chip
                label="Live Data"
                color="success"
                size="small"
                variant="outlined"
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Total Profit */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <ProfitIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6" color="text.secondary">
                  Total Profit
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
                {formatCurrency(metrics.total_profit)}
              </Typography>
              <Chip
                label="Live Data"
                color="success"
                size="small"
                variant="outlined"
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Profit Margin */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <TrendingUpIcon 
                  color={getMetricColor('margin', metrics.profit_margin) as any} 
                  sx={{ mr: 1 }} 
                />
                <Typography variant="h6" color="text.secondary">
                  Profit Margin
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
                {formatPercentage(metrics.profit_margin)}
              </Typography>
              <Chip
                label={metrics.profit_margin > 20 ? "Excellent" : metrics.profit_margin > 10 ? "Good" : "Needs Attention"}
                color={getMetricColor('margin', metrics.profit_margin) as any}
                size="small"
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Total Customers */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <CustomerIcon color="info" sx={{ mr: 1 }} />
                <Typography variant="h6" color="text.secondary">
                  Total Customers
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
                {formatNumber(metrics.total_customers)}
              </Typography>
              <Chip
                label="Active"
                color="info"
                size="small"
                variant="outlined"
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Secondary Metrics */}
      <Grid container spacing={3}>
        {/* Average Order Value */}
        <Grid item xs={12} sm={6} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <OrderIcon color="secondary" sx={{ mr: 1 }} />
                <Typography variant="h6" color="text.secondary">
                  Average Order Value
                </Typography>
              </Box>
              <Typography variant="h3" sx={{ fontWeight: 600, mb: 1 }}>
                {formatCurrency(metrics.average_order_value)}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Per customer transaction
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Inventory Turnover */}
        <Grid item xs={12} sm={6} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <InventoryIcon 
                  color={getMetricColor('turnover', metrics.inventory_turnover) as any} 
                  sx={{ mr: 1 }} 
                />
                <Typography variant="h6" color="text.secondary">
                  Inventory Turnover
                </Typography>
              </Box>
              <Typography variant="h3" sx={{ fontWeight: 600, mb: 1 }}>
                {metrics.inventory_turnover.toFixed(1)}x
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Times per year
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Performance Summary */}
      <Card sx={{ mt: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Performance Summary
          </Typography>
          <Divider sx={{ mb: 2 }} />
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="success.main" sx={{ fontWeight: 600 }}>
                  {formatPercentage(metrics.profit_margin)}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Profit Margin
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="primary.main" sx={{ fontWeight: 600 }}>
                  {formatCurrency(metrics.average_order_value)}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Average Order Value
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="info.main" sx={{ fontWeight: 600 }}>
                  {metrics.inventory_turnover.toFixed(1)}x
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Inventory Turnover Rate
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
} 