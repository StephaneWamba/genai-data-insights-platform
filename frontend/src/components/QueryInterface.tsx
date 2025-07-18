import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Chip,
  CircularProgress,
  Alert,
  Grid,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  LinearProgress,
  Paper,
} from '@mui/material';
import {
  Send as SendIcon,
  Lightbulb as InsightIcon,
  TrendingUp as TrendIcon,
  Psychology as IntentIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
  AutoAwesome as AutoAwesomeIcon,
  BarChart as ChartIcon,
  Analytics as AnalyticsIcon,
  Psychology as PsychologyIcon,
} from '@mui/icons-material';
import { useQuery } from '../contexts/QueryContext';
import { queryAPI } from '../services/api';
import ChartDisplay from './ChartDisplay';

// Sample query suggestions
const querySuggestions = [
  "Show me a bar chart of top 5 products by revenue",
  "Create a pie chart of revenue distribution by store",
  "Show me a doughnut chart of sales by category",
  "Create a horizontal bar chart of store performance",
  "Show me a bubble chart of revenue vs quantity vs profit",
  "Create a radar chart of product performance metrics",
  "Show me a stacked bar chart of sales by region",
  "Create a multi-line chart of revenue trends over time",
  "What are the sales trends for shoes in Paris stores this quarter?",
  "Which products have the highest profit margins?",
  "Show me customer segments with declining purchase frequency",
  "What's the inventory status for electronics category?",
  "Analyze sales performance by store location",
  "Which customers are at risk of churning?",
  "What are the top-selling products this month?",
  "Show me revenue trends over the last 6 months",
];

export default function QueryInterface() {
  const { state, dispatch } = useQuery();
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [buttonColor, setButtonColor] = useState('primary');

  const handleQuerySubmit = async () => {
    if (!inputValue.trim()) return;

    setIsProcessing(true);
    setButtonColor('success');
    dispatch({ type: 'SET_LOADING', payload: true });
    dispatch({ type: 'SET_ERROR', payload: null });
    dispatch({ type: 'SET_CURRENT_QUERY', payload: inputValue });

    try {
      const response = await queryAPI.processQuery(inputValue, 'user123');
      dispatch({ type: 'SET_RESPONSE', payload: response });
      dispatch({ type: 'ADD_TO_HISTORY', payload: response.query });
      setInputValue('');
      setButtonColor('success');
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || 'Failed to process query';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      setButtonColor('error');
    } finally {
      setIsProcessing(false);
      dispatch({ type: 'SET_LOADING', payload: false });
      // Reset button color after a delay
      setTimeout(() => setButtonColor('primary'), 2000);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInputValue(suggestion);
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleQuerySubmit();
    }
  };

  const formatConfidenceScore = (score: number) => {
    return `${(score * 100).toFixed(0)}%`;
  };

  const getConfidenceColor = (score: number) => {
    if (score >= 0.8) return 'success';
    if (score >= 0.6) return 'warning';
    return 'error';
  };

  // Function to highlight important numbers and metrics in text
  const highlightImportantPoints = (text: string) => {
    // Highlight currency amounts, percentages, and key metrics
    const highlightedText = text.replace(
      /(\$[\d,]+\.?\d*)|(\d+\.?\d*%)|(\d+\.?\d*)/g,
      (match, currency, percentage, number) => {
        if (currency) {
          return `<span style="color: #1976d2; font-weight: 600; background-color: rgba(25, 118, 210, 0.1); padding: 2px 4px; border-radius: 4px;">${match}</span>`;
        }
        if (percentage) {
          return `<span style="color: #2e7d32; font-weight: 600; background-color: rgba(46, 125, 50, 0.1); padding: 2px 4px; border-radius: 4px;">${match}</span>`;
        }
        if (number && parseFloat(number) > 1000) {
          return `<span style="color: #ed6c02; font-weight: 600; background-color: rgba(237, 108, 2, 0.1); padding: 2px 4px; border-radius: 4px;">${match}</span>`;
        }
        return match;
      }
    );
    return highlightedText;
  };

  return (
    <Box sx={{ maxWidth: 1400, mx: 'auto', p: 2 }}>
      {/* Enhanced Header */}
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography 
          variant="h3" 
          gutterBottom 
          sx={{ 
            fontWeight: 700, 
            background: 'linear-gradient(45deg, #1976d2, #42a5f5)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            mb: 2
          }}
        >
          AI-Powered Business Intelligence
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ fontWeight: 400 }}>
          Ask questions about your business data in plain English and get instant insights
        </Typography>
      </Box>

      {/* Enhanced Query Input Section */}
      <Card sx={{ 
        mb: 4, 
        background: 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
        boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
        border: '1px solid #e0e0e0'
      }}>
        <CardContent sx={{ p: 5 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
            <PsychologyIcon sx={{ mr: 3, fontSize: 36, color: '#1976d2' }} />
            <Typography variant="h4" sx={{ 
              fontWeight: 700, 
              color: '#2c3e50',
              textShadow: '0 1px 2px rgba(0,0,0,0.1)'
            }}>
              Ask Your Question
            </Typography>
          </Box>
          
          <TextField
            fullWidth
            multiline
            rows={5}
            variant="outlined"
            placeholder="e.g., What are the sales trends for shoes in Paris stores this quarter?"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isProcessing}
            sx={{ 
              mb: 4,
              '& .MuiOutlinedInput-root': {
                backgroundColor: 'white',
                borderRadius: 3,
                fontSize: '1.1rem',
                '& .MuiOutlinedInput-input': {
                  color: '#2c3e50',
                  fontWeight: 500,
                  '&::placeholder': {
                    color: '#7f8c8d',
                    opacity: 1,
                    fontWeight: 400,
                  },
                },
                '& .MuiOutlinedInput-notchedOutline': {
                  borderColor: '#bdc3c7',
                  borderWidth: 2,
                },
                '&:hover': {
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#1976d2',
                    borderWidth: 2,
                  },
                },
                '&.Mui-focused': {
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#1976d2',
                    borderWidth: 3,
                  },
                },
              },
            }}
          />

          <Box sx={{ display: 'flex', gap: 3, mb: 5 }}>
            <Button
              variant="contained"
              size="large"
              startIcon={isProcessing ? <CircularProgress size={24} /> : <SendIcon />}
              onClick={handleQuerySubmit}
              disabled={!inputValue.trim() || isProcessing}
              color={buttonColor as any}
              sx={{ 
                minWidth: 160,
                height: 56,
                fontSize: '1.1rem',
                fontWeight: 600,
                boxShadow: buttonColor === 'success' 
                  ? '0 4px 15px rgba(76, 175, 80, 0.4)' 
                  : buttonColor === 'error'
                  ? '0 4px 15px rgba(244, 67, 54, 0.4)'
                  : '0 4px 15px rgba(25, 118, 210, 0.3)',
                '&:hover': {
                  boxShadow: buttonColor === 'success' 
                    ? '0 6px 20px rgba(76, 175, 80, 0.5)' 
                    : buttonColor === 'error'
                    ? '0 6px 20px rgba(244, 67, 54, 0.5)'
                    : '0 6px 20px rgba(25, 118, 210, 0.4)',
                  transform: 'translateY(-2px)',
                },
                '&:disabled': {
                  boxShadow: 'none',
                  transform: 'none',
                },
              }}
            >
              {isProcessing ? 'Processing...' : 'Ask Question'}
            </Button>
            
            <Button
              variant="outlined"
              size="large"
              onClick={() => setInputValue('')}
              disabled={!inputValue.trim() || isProcessing}
              sx={{
                height: 56,
                fontSize: '1.1rem',
                fontWeight: 600,
                borderColor: '#7f8c8d',
                color: '#2c3e50',
                '&:hover': {
                  borderColor: '#1976d2',
                  backgroundColor: 'rgba(25, 118, 210, 0.05)',
                  transform: 'translateY(-1px)',
                },
              }}
            >
              Clear
            </Button>
          </Box>

          {/* Enhanced Query Suggestions */}
          <Box>
            <Typography variant="h5" gutterBottom sx={{ 
              mb: 3, 
              fontWeight: 700,
              color: '#2c3e50',
              textShadow: '0 1px 2px rgba(0,0,0,0.1)'
            }}>
              Try these example queries:
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
              {querySuggestions.map((suggestion, index) => (
                <Chip
                  key={index}
                  label={suggestion}
                  variant="outlined"
                  size="medium"
                  onClick={() => handleSuggestionClick(suggestion)}
                  sx={{ 
                    cursor: 'pointer',
                    fontSize: '0.95rem',
                    fontWeight: 500,
                    borderColor: '#bdc3c7',
                    color: '#2c3e50',
                    backgroundColor: 'rgba(255,255,255,0.8)',
                    '&:hover': {
                      backgroundColor: '#1976d2',
                      color: 'white',
                      borderColor: '#1976d2',
                      transform: 'translateY(-2px)',
                      boxShadow: '0 4px 12px rgba(25, 118, 210, 0.3)',
                      transition: 'all 0.3s ease-in-out',
                    },
                  }}
                />
              ))}
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* Loading and Error States */}
      {state.isLoading && (
        <Card sx={{ mb: 4, background: 'linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%)' }}>
          <CardContent sx={{ p: 4, textAlign: 'center' }}>
            <CircularProgress size={40} sx={{ mb: 2 }} />
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              Processing your query...
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Our AI is analyzing your data and generating insights
            </Typography>
            <LinearProgress sx={{ mt: 2 }} />
          </CardContent>
        </Card>
      )}

      {state.error && (
        <Card sx={{ mb: 4, background: 'linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%)' }}>
          <CardContent sx={{ p: 4 }}>
            <Alert severity="error" icon={<ErrorIcon />} sx={{ fontSize: '1.1rem' }}>
              {state.error}
            </Alert>
          </CardContent>
        </Card>
      )}

      {/* Enhanced Results Section - Side by Side Layout */}
      {state.currentResponse && (
        <Grid container spacing={5}>
          {/* Left Column - AI Insights */}
          <Grid item xs={12} lg={6}>
            <Card sx={{ 
              minHeight: '600px',
              background: 'linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%)',
              boxShadow: '0 12px 40px rgba(0,0,0,0.15)',
              borderRadius: 4,
              border: '1px solid rgba(25, 118, 210, 0.1)'
            }}>
              <CardContent sx={{ p: 5 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
                  <InsightIcon sx={{ mr: 3, fontSize: 40, color: '#1976d2' }} />
                  <Typography variant="h4" sx={{ 
                    fontWeight: 700,
                    color: '#2c3e50',
                    textShadow: '0 1px 2px rgba(0,0,0,0.1)'
                  }}>
                    AI-Generated Insights
                  </Typography>
                </Box>

                {/* Intent Analysis */}
                <Paper sx={{ 
                  p: 4, 
                  mb: 4, 
                  backgroundColor: 'rgba(255,255,255,0.9)',
                  borderRadius: 3,
                  boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
                  border: '1px solid rgba(25, 118, 210, 0.1)'
                }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                    <IntentIcon sx={{ mr: 2, fontSize: 28, color: '#1976d2' }} />
                    <Typography variant="h5" sx={{ 
                      fontWeight: 700,
                      color: '#2c3e50'
                    }}>
                      Query Intent Analysis
                    </Typography>
                  </Box>
                  <Grid container spacing={3}>
                    <Grid item xs={6}>
                      <Typography variant="h6" sx={{ 
                        color: '#7f8c8d',
                        fontWeight: 600,
                        mb: 1
                      }}>
                        Intent Type
                      </Typography>
                      <Typography variant="h5" sx={{ 
                        fontWeight: 700, 
                        color: '#1976d2',
                        textTransform: 'capitalize'
                      }}>
                        {state.currentResponse.intent.intent.replace('_', ' ')}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="h6" sx={{ 
                        color: '#7f8c8d',
                        fontWeight: 600,
                        mb: 1
                      }}>
                        Confidence
                      </Typography>
                      <Chip
                        label={formatConfidenceScore(state.currentResponse.intent.confidence)}
                        color={getConfidenceColor(state.currentResponse.intent.confidence) as any}
                        size="medium"
                        sx={{ 
                          fontWeight: 700,
                          fontSize: '1rem',
                          height: 40
                        }}
                      />
                    </Grid>
                  </Grid>
                </Paper>

                {/* Enhanced Insights */}
                <Box>
                  {state.currentResponse.insights.map((insight, index) => (
                    <Paper 
                      key={index} 
                      sx={{ 
                        p: 4, 
                        mb: 4, 
                        backgroundColor: 'rgba(255,255,255,0.95)',
                        borderRadius: 3,
                        borderLeft: '6px solid #1976d2',
                        boxShadow: '0 6px 25px rgba(0,0,0,0.1)',
                        '&:hover': {
                          transform: 'translateY(-3px)',
                          boxShadow: '0 8px 30px rgba(0,0,0,0.2)',
                          transition: 'all 0.3s ease-in-out',
                        }
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 3 }}>
                        <AutoAwesomeIcon sx={{ mr: 3, mt: 0.5, fontSize: 32, color: '#1976d2' }} />
                        <Box sx={{ flex: 1 }}>
                          <Typography variant="h5" sx={{ 
                            fontWeight: 700, 
                            mb: 2,
                            color: '#2c3e50',
                            lineHeight: 1.3
                          }}>
                            {insight.title}
                          </Typography>
                          <Typography 
                            variant="h6" 
                            sx={{ 
                              mb: 3, 
                              lineHeight: 1.7,
                              color: '#34495e',
                              fontWeight: 500,
                              '& span': {
                                display: 'inline',
                              }
                            }}
                            dangerouslySetInnerHTML={{ 
                              __html: highlightImportantPoints(insight.description) 
                            }}
                          />
                          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                            <Chip
                              label={insight.category}
                              size="medium"
                              variant="outlined"
                              sx={{ 
                                fontWeight: 700,
                                fontSize: '0.9rem',
                                borderColor: '#1976d2',
                                color: '#1976d2'
                              }}
                            />
                            <Chip
                              label={`Confidence: ${formatConfidenceScore(insight.confidence_score)}`}
                              size="medium"
                              color={getConfidenceColor(insight.confidence_score) as any}
                              sx={{ 
                                fontWeight: 700,
                                fontSize: '0.9rem',
                                height: 40
                              }}
                            />
                          </Box>
                        </Box>
                      </Box>
                    </Paper>
                  ))}
                </Box>

                {/* Enhanced Recommendations */}
                {state.currentResponse.recommendations.length > 0 && (
                  <Paper sx={{ p: 3, backgroundColor: 'rgba(255,255,255,0.8)' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <TrendIcon sx={{ mr: 2, color: 'success.main' }} />
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        Actionable Recommendations
                      </Typography>
                    </Box>
                    <List>
                      {state.currentResponse.recommendations.map((recommendation, index) => (
                        <ListItem key={index} sx={{ px: 0 }}>
                          <ListItemIcon>
                            <SuccessIcon color="success" />
                          </ListItemIcon>
                          <ListItemText 
                            primary={recommendation}
                            primaryTypographyProps={{
                              variant: 'body1',
                              sx: { fontWeight: 500 }
                            }}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </Paper>
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* Right Column - Charts and Visualizations */}
          <Grid item xs={12} lg={6}>
            {state.currentResponse.visualizations && state.currentResponse.visualizations.length > 0 ? (
              <Card sx={{ 
                minHeight: '600px',
                background: 'linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%)',
                boxShadow: '0 12px 40px rgba(0,0,0,0.15)',
                borderRadius: 4,
                border: '1px solid rgba(156, 39, 176, 0.1)'
              }}>
                <CardContent sx={{ p: 5 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
                    <ChartIcon sx={{ mr: 3, fontSize: 40, color: '#9c27b0' }} />
                    <Typography variant="h4" sx={{ 
                      fontWeight: 700,
                      color: '#2c3e50',
                      textShadow: '0 1px 2px rgba(0,0,0,0.1)'
                    }}>
                      Data Visualizations
                    </Typography>
                  </Box>
                  
                  {state.currentResponse.visualizations.map((visualization, index) => (
                    <Box key={index} sx={{ mb: 4 }}>
                      <ChartDisplay visualization={visualization} />
                    </Box>
                  ))}
                </CardContent>
              </Card>
            ) : (
              <Card sx={{ 
                minHeight: '600px',
                background: 'linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%)',
                boxShadow: '0 12px 40px rgba(0,0,0,0.15)',
                borderRadius: 4,
                border: '1px solid rgba(156, 39, 176, 0.1)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <CardContent sx={{ p: 5, textAlign: 'center' }}>
                  <AnalyticsIcon sx={{ fontSize: 80, color: '#9c27b0', mb: 3 }} />
                  <Typography variant="h5" sx={{ 
                    fontWeight: 700, 
                    mb: 2,
                    color: '#2c3e50'
                  }}>
                    No Visualizations Available
                  </Typography>
                  <Typography variant="h6" sx={{ 
                    color: '#7f8c8d',
                    fontWeight: 500
                  }}>
                    Try asking for specific chart types like "bar chart", "pie chart", or "line chart"
                  </Typography>
                </CardContent>
              </Card>
            )}
          </Grid>
        </Grid>
      )}
    </Box>
  );
} 