import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  RadialLinearScale,
} from 'chart.js';
import { Bar, Line, Pie, Scatter, Doughnut, Bubble, Radar } from 'react-chartjs-2';
import { Box, Typography, Chip, Paper } from '@mui/material';
import { Analytics as AnalyticsIcon } from '@mui/icons-material';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  RadialLinearScale
);

// Set default Chart.js options
ChartJS.defaults.responsive = true;
ChartJS.defaults.maintainAspectRatio = false;

interface ChartDisplayProps {
  visualization: {
    type: string;
    title: string;
    chart_data?: any;
    data_points?: number;
    columns_used?: string[];
    data_source: string;
  };
}

export default function ChartDisplay({ visualization }: ChartDisplayProps) {
  const { type, title, chart_data, data_points, columns_used, data_source } = visualization;

  const renderChart = () => {
    if (!chart_data) {
      return (
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 200 }}>
          <Typography variant="body2" color="text.secondary">
            Chart data not available
          </Typography>
        </Box>
      );
    }
    
    try {
      switch (type) {
        case 'bar_chart':
          return <Bar data={chart_data.data} options={chart_data.options} />;
        case 'line_chart':
          return <Line data={chart_data.data} options={chart_data.options} />;
        case 'pie_chart':
          const pieOptions = {
            ...chart_data.options,
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              ...chart_data.options?.plugins,
              legend: {
                ...chart_data.options?.plugins?.legend,
                display: true,
                position: 'bottom' as const,
              },
            },
          };
          return <Pie data={chart_data.data} options={pieOptions} />;
        case 'scatter_plot':
          return <Scatter data={chart_data.data} options={chart_data.options} />;
        case 'area_chart':
          return <Line data={chart_data.data} options={chart_data.options} />;
        case 'doughnut_chart':
          return <Doughnut data={chart_data.data} options={chart_data.options} />;
        case 'horizontal_bar_chart':
          return <Bar data={chart_data.data} options={chart_data.options} />;
        case 'bubble_chart':
          return <Bubble data={chart_data.data} options={chart_data.options} />;
        case 'radar_chart':
          return <Radar data={chart_data.data} options={chart_data.options} />;
        case 'stacked_bar_chart':
          return <Bar data={chart_data.data} options={chart_data.options} />;
        case 'multi_line_chart':
          return <Line data={chart_data.data} options={chart_data.options} />;
        default:
          return <Bar data={chart_data.data} options={chart_data.options} />;
      }
    } catch (error) {
      return (
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 200 }}>
          <Typography variant="body2" color="error">
            Error rendering chart
          </Typography>
        </Box>
      );
    }
  };

  return (
    <Paper sx={{ 
      p: 4, 
      backgroundColor: 'rgba(255,255,255,0.98)',
      borderRadius: 4,
      boxShadow: '0 6px 25px rgba(0,0,0,0.12)',
      border: '1px solid rgba(156, 39, 176, 0.1)',
      '&:hover': {
        transform: 'translateY(-3px)',
        boxShadow: '0 10px 35px rgba(0,0,0,0.2)',
        transition: 'all 0.3s ease-in-out',
      }
    }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
        <AnalyticsIcon sx={{ mr: 3, fontSize: 32, color: '#9c27b0' }} />
        <Typography variant="h5" component="div" sx={{ 
          fontWeight: 700,
          color: '#2c3e50'
        }}>
          {title}
        </Typography>
      </Box>
      
      <Box sx={{ height: 450, mb: 4, position: 'relative' }}>
        {renderChart()}
      </Box>
      
      {/* Enhanced metadata */}
      <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
        <Chip 
          label={type.replace('_', ' ').toUpperCase()} 
          size="medium" 
          variant="outlined"
          sx={{ 
            fontWeight: 700,
            fontSize: '0.9rem',
            backgroundColor: '#9c27b0',
            color: 'white',
            borderColor: '#9c27b0',
            '& .MuiChip-label': {
              color: 'white',
            }
          }}
        />
        {data_points && (
          <Chip 
            label={`${data_points} data points`} 
            size="medium" 
            variant="outlined"
            sx={{ 
              fontWeight: 700,
              fontSize: '0.9rem',
              borderColor: '#7f8c8d',
              color: '#2c3e50'
            }}
          />
        )}
        {columns_used && columns_used.length > 0 && (
          <Chip 
            label={`Columns: ${columns_used.join(', ')}`} 
            size="medium" 
            variant="outlined"
            sx={{ 
              fontWeight: 700,
              fontSize: '0.9rem',
              borderColor: '#7f8c8d',
              color: '#2c3e50'
            }}
          />
        )}
        <Chip 
          label={`Source: ${data_source}`} 
          size="medium" 
          variant="outlined"
          sx={{ 
            fontWeight: 700,
            fontSize: '0.9rem',
            borderColor: '#7f8c8d',
            color: '#2c3e50'
          }}
        />
      </Box>
      

    </Paper>
  );
} 