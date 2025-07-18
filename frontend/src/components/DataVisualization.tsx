import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
  Alert,
  Chip,
  Grid,
  Tabs,
  Tab,
  TablePagination,
  TextField,
  InputAdornment,
} from '@mui/material';
import {
  Search as SearchIcon,
  TrendingUp as TrendingUpIcon,
  Inventory as InventoryIcon,
  People as PeopleIcon,
  AttachMoney as MoneyIcon,
} from '@mui/icons-material';
import { useData } from '../contexts/DataContext';
import { dataAPI } from '../services/api';

interface DataVisualizationProps {
  dataType?: 'sales' | 'inventory' | 'customers';
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`data-tabpanel-${index}`}
      aria-labelledby={`data-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

export default function DataVisualization({ dataType = 'sales' }: DataVisualizationProps) {
  const { state, dispatch } = useData();
  const [tabValue, setTabValue] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  useEffect(() => {
    const fetchData = async () => {
      dispatch({ type: 'SET_LOADING', payload: true });
      try {
        switch (dataType) {
          case 'sales':
            const salesData = await dataAPI.getSalesData(30);
            dispatch({ type: 'SET_SALES_DATA', payload: salesData });
            break;
          case 'inventory':
            const inventoryData = await dataAPI.getInventoryData();
            dispatch({ type: 'SET_INVENTORY_DATA', payload: inventoryData });
            break;
          case 'customers':
            const customerData = await dataAPI.getCustomerData(100);
            dispatch({ type: 'SET_CUSTOMER_DATA', payload: customerData });
            break;
        }
      } catch (error: any) {
        const errorMessage = error.response?.data?.message || `Failed to load ${dataType} data`;
        dispatch({ type: 'SET_ERROR', payload: errorMessage });
      } finally {
        dispatch({ type: 'SET_LOADING', payload: false });
      }
    };

    fetchData();
  }, [dataType, dispatch]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const getDataIcon = () => {
    switch (dataType) {
      case 'sales':
        return <MoneyIcon />;
      case 'inventory':
        return <InventoryIcon />;
      case 'customers':
        return <PeopleIcon />;
      default:
        return <TrendingUpIcon />;
    }
  };

  const getDataTitle = () => {
    switch (dataType) {
      case 'sales':
        return 'Sales Data';
      case 'inventory':
        return 'Inventory Status';
      case 'customers':
        return 'Customer Insights';
      default:
        return 'Data Analytics';
    }
  };

  const getDataDescription = () => {
    switch (dataType) {
      case 'sales':
        return 'Real-time sales performance and revenue analytics';
      case 'inventory':
        return 'Current inventory levels and stock management';
      case 'customers':
        return 'Customer segmentation and purchase behavior';
      default:
        return 'Comprehensive data analysis and insights';
    }
  };

  const filterData = (data: any[]) => {
    if (!searchTerm) return data;
    
    return data.filter((item) => {
      const searchLower = searchTerm.toLowerCase();
      return Object.values(item).some((value) =>
        String(value).toLowerCase().includes(searchLower)
      );
    });
  };

  const getFilteredData = () => {
    switch (dataType) {
      case 'sales':
        return filterData(state.sales);
      case 'inventory':
        return filterData(state.inventory);
      case 'customers':
        return filterData(state.customers);
      default:
        return [];
    }
  };

  const filteredData = getFilteredData();
  const paginatedData = filteredData.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

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

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          {getDataIcon()}
          <Typography variant="h4" sx={{ ml: 1, fontWeight: 600 }}>
            {getDataTitle()}
          </Typography>
        </Box>
        <Typography variant="body1" color="text.secondary">
          {getDataDescription()}
        </Typography>
      </Box>

      {/* Search and Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                placeholder="Search data..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
                <Chip
                  label={`${filteredData.length} records`}
                  color="primary"
                  variant="outlined"
                />
                <Chip
                  label="Live Data"
                  color="success"
                  size="small"
                />
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Data Table */}
      <Card>
        <CardContent>
          <TableContainer component={Paper} sx={{ maxHeight: 600 }}>
            <Table stickyHeader>
              <TableHead>
                {dataType === 'sales' && (
                  <TableRow>
                    <TableCell>Date</TableCell>
                    <TableCell>Product</TableCell>
                    <TableCell>Category</TableCell>
                    <TableCell>Store</TableCell>
                    <TableCell align="right">Quantity</TableCell>
                    <TableCell align="right">Revenue</TableCell>
                    <TableCell align="right">Profit</TableCell>
                  </TableRow>
                )}
                {dataType === 'inventory' && (
                  <TableRow>
                    <TableCell>Product</TableCell>
                    <TableCell>Category</TableCell>
                    <TableCell>Store</TableCell>
                    <TableCell align="right">Current Stock</TableCell>
                    <TableCell align="right">Reorder Level</TableCell>
                    <TableCell>Supplier</TableCell>
                    <TableCell>Status</TableCell>
                  </TableRow>
                )}
                {dataType === 'customers' && (
                  <TableRow>
                    <TableCell>Customer ID</TableCell>
                    <TableCell>Name</TableCell>
                    <TableCell>Email</TableCell>
                    <TableCell>Segment</TableCell>
                    <TableCell align="right">Total Purchases</TableCell>
                    <TableCell>Last Purchase</TableCell>
                  </TableRow>
                )}
              </TableHead>
              <TableBody>
                {paginatedData.map((row, index) => (
                  <TableRow key={index} hover>
                    {dataType === 'sales' && (
                      <>
                        <TableCell>{formatDate(row.date)}</TableCell>
                        <TableCell>{row.product}</TableCell>
                        <TableCell>{row.category}</TableCell>
                        <TableCell>{row.store}</TableCell>
                        <TableCell align="right">{row.quantity}</TableCell>
                        <TableCell align="right">{formatCurrency(row.revenue)}</TableCell>
                        <TableCell align="right">{formatCurrency(row.profit)}</TableCell>
                      </>
                    )}
                    {dataType === 'inventory' && (
                      <>
                        <TableCell>{row.product}</TableCell>
                        <TableCell>{row.category}</TableCell>
                        <TableCell>{row.store}</TableCell>
                        <TableCell align="right">{row.quantity}</TableCell>
                        <TableCell align="right">{row.reorder_level}</TableCell>
                        <TableCell>{row.supplier}</TableCell>
                        <TableCell>
                          <Chip
                            label={row.quantity <= row.reorder_level ? 'Low Stock' : 'In Stock'}
                            color={row.quantity <= row.reorder_level ? 'error' : 'success'}
                            size="small"
                          />
                        </TableCell>
                      </>
                    )}
                    {dataType === 'customers' && (
                      <>
                        <TableCell>{row.customer_id}</TableCell>
                        <TableCell>{row.name}</TableCell>
                        <TableCell>{row.email}</TableCell>
                        <TableCell>
                          <Chip label={row.segment} size="small" variant="outlined" />
                        </TableCell>
                        <TableCell align="right">{row.total_purchases}</TableCell>
                        <TableCell>{formatDate(row.last_purchase_date)}</TableCell>
                      </>
                    )}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
          
          <TablePagination
            rowsPerPageOptions={[5, 10, 25, 50]}
            component="div"
            count={filteredData.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </CardContent>
      </Card>

      {/* Summary Statistics */}
      {filteredData.length > 0 && (
        <Card sx={{ mt: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Summary Statistics
            </Typography>
            <Grid container spacing={3}>
              {dataType === 'sales' && (
                <>
                  <Grid item xs={12} sm={6} md={3}>
                    <Typography variant="body2" color="text.secondary">
                      Total Revenue
                    </Typography>
                    <Typography variant="h6">
                      {formatCurrency(filteredData.reduce((sum, item) => sum + item.revenue, 0))}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Typography variant="body2" color="text.secondary">
                      Total Profit
                    </Typography>
                    <Typography variant="h6">
                      {formatCurrency(filteredData.reduce((sum, item) => sum + item.profit, 0))}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Typography variant="body2" color="text.secondary">
                      Total Quantity
                    </Typography>
                    <Typography variant="h6">
                      {filteredData.reduce((sum, item) => sum + item.quantity, 0).toLocaleString()}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Typography variant="body2" color="text.secondary">
                      Unique Products
                    </Typography>
                    <Typography variant="h6">
                      {new Set(filteredData.map(item => item.product)).size}
                    </Typography>
                  </Grid>
                </>
              )}
              {dataType === 'inventory' && (
                <>
                  <Grid item xs={12} sm={6} md={3}>
                    <Typography variant="body2" color="text.secondary">
                      Total Items
                    </Typography>
                    <Typography variant="h6">
                      {filteredData.reduce((sum, item) => sum + item.quantity, 0).toLocaleString()}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Typography variant="body2" color="text.secondary">
                      Low Stock Items
                    </Typography>
                    <Typography variant="h6">
                      {filteredData.filter(item => item.quantity <= item.reorder_level).length}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Typography variant="body2" color="text.secondary">
                      Unique Products
                    </Typography>
                    <Typography variant="h6">
                      {new Set(filteredData.map(item => item.product)).size}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Typography variant="body2" color="text.secondary">
                      Unique Suppliers
                    </Typography>
                    <Typography variant="h6">
                      {new Set(filteredData.map(item => item.supplier)).size}
                    </Typography>
                  </Grid>
                </>
              )}
              {dataType === 'customers' && (
                <>
                  <Grid item xs={12} sm={6} md={3}>
                    <Typography variant="body2" color="text.secondary">
                      Total Customers
                    </Typography>
                    <Typography variant="h6">
                      {filteredData.length}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Typography variant="body2" color="text.secondary">
                      Total Purchases
                    </Typography>
                    <Typography variant="h6">
                      {filteredData.reduce((sum, item) => sum + item.total_purchases, 0).toLocaleString()}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Typography variant="body2" color="text.secondary">
                      Average Purchases
                    </Typography>
                    <Typography variant="h6">
                      {(filteredData.reduce((sum, item) => sum + item.total_purchases, 0) / filteredData.length).toFixed(1)}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Typography variant="body2" color="text.secondary">
                      Unique Segments
                    </Typography>
                    <Typography variant="h6">
                      {new Set(filteredData.map(item => item.segment)).size}
                    </Typography>
                  </Grid>
                </>
              )}
            </Grid>
          </CardContent>
        </Card>
      )}
    </Box>
  );
} 