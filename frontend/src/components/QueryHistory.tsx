import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Grid,
  Alert,
} from '@mui/material';
import {
  History as HistoryIcon,
  QueryStats as QueryIcon,
  Lightbulb as InsightIcon,
  TrendingUp as TrendIcon,
  Psychology as IntentIcon,
  ExpandMore as ExpandMoreIcon,
  AutoAwesome as AutoAwesomeIcon,
  CheckCircle as SuccessIcon,
} from '@mui/icons-material';
import { useQuery } from '../contexts/QueryContext';

export default function QueryHistory() {
  const { state } = useQuery();

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatConfidenceScore = (score: number) => {
    return `${(score * 100).toFixed(0)}%`;
  };

  const getConfidenceColor = (score: number) => {
    if (score >= 0.8) return 'success';
    if (score >= 0.6) return 'warning';
    return 'error';
  };

  if (state.queryHistory.length === 0) {
    return (
      <Box>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
            Query History
          </Typography>
          <Typography variant="body1" color="text.secondary">
            View your past queries and AI-generated insights
          </Typography>
        </Box>
        
        <Alert severity="info">
          No queries in history yet. Start by asking a question in the Natural Language Query section!
        </Alert>
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <HistoryIcon sx={{ mr: 1 }} />
          <Typography variant="h4" sx={{ fontWeight: 600 }}>
            Query History
          </Typography>
        </Box>
        <Typography variant="body1" color="text.secondary">
          View your past queries and AI-generated insights
        </Typography>
      </Box>

      {/* Query History List */}
      <List>
        {state.queryHistory.map((query, index) => (
          <Card key={index} sx={{ mb: 3 }}>
            <CardContent>
              {/* Query Header */}
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <QueryIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6" sx={{ flexGrow: 1 }}>
                  {query.text}
                </Typography>
                <Chip
                  label={formatDate(query.created_at)}
                  size="small"
                  variant="outlined"
                />
              </Box>

              {/* Query Status */}
              <Box sx={{ mb: 2 }}>
                <Chip
                  label={query.processed ? 'Processed' : 'Pending'}
                  color={query.processed ? 'success' : 'warning'}
                  size="small"
                  icon={query.processed ? <SuccessIcon /> : undefined}
                />
              </Box>

              {/* Query Response */}
              {query.response && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    {query.response}
                  </Typography>
                </Box>
              )}

              <Divider sx={{ my: 2 }} />

              {/* Detailed Results (if available) */}
              {state.currentResponse && state.currentResponse.query.id === query.id && (
                <Box>
                  {/* Intent Analysis */}
                  <Accordion>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <IntentIcon sx={{ mr: 1 }} />
                        <Typography variant="subtitle1">Query Intent Analysis</Typography>
                      </Box>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Grid container spacing={2}>
                        <Grid item xs={12} sm={6}>
                          <Typography variant="body2" color="text.secondary">
                            Intent Type
                          </Typography>
                          <Typography variant="body1" sx={{ fontWeight: 500 }}>
                            {state.currentResponse.intent.intent}
                          </Typography>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                          <Typography variant="body2" color="text.secondary">
                            Confidence
                          </Typography>
                          <Chip
                            label={formatConfidenceScore(state.currentResponse.intent.confidence)}
                            color={getConfidenceColor(state.currentResponse.intent.confidence) as any}
                            size="small"
                          />
                        </Grid>
                      </Grid>
                    </AccordionDetails>
                  </Accordion>

                  {/* Insights */}
                  <Accordion>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <InsightIcon sx={{ mr: 1 }} />
                        <Typography variant="subtitle1">
                          AI-Generated Insights ({state.currentResponse.insights.length})
                        </Typography>
                      </Box>
                    </AccordionSummary>
                    <AccordionDetails>
                      <List>
                        {state.currentResponse.insights.map((insight, insightIndex) => (
                          <ListItem key={insightIndex} sx={{ px: 0 }}>
                            <ListItemIcon>
                              <AutoAwesomeIcon color="primary" />
                            </ListItemIcon>
                            <ListItemText
                              primary={insight.title}
                              secondary={
                                <Box>
                                  <Typography variant="body2" sx={{ mb: 1 }}>
                                    {insight.description}
                                  </Typography>
                                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                                    <Chip
                                      label={insight.category}
                                      size="small"
                                      variant="outlined"
                                    />
                                    <Chip
                                      label={`Confidence: ${formatConfidenceScore(insight.confidence_score)}`}
                                      size="small"
                                      color={getConfidenceColor(insight.confidence_score) as any}
                                    />
                                  </Box>
                                </Box>
                              }
                            />
                          </ListItem>
                        ))}
                      </List>
                    </AccordionDetails>
                  </Accordion>

                  {/* Recommendations */}
                  {state.currentResponse.recommendations.length > 0 && (
                    <Accordion>
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <TrendIcon sx={{ mr: 1 }} />
                          <Typography variant="subtitle1">
                            Actionable Recommendations ({state.currentResponse.recommendations.length})
                          </Typography>
                        </Box>
                      </AccordionSummary>
                      <AccordionDetails>
                        <List>
                          {state.currentResponse.recommendations.map((recommendation, recIndex) => (
                            <ListItem key={recIndex} sx={{ px: 0 }}>
                              <ListItemIcon>
                                <SuccessIcon color="success" />
                              </ListItemIcon>
                              <ListItemText primary={recommendation} />
                            </ListItem>
                          ))}
                        </List>
                      </AccordionDetails>
                    </Accordion>
                  )}
                </Box>
              )}
            </CardContent>
          </Card>
        ))}
      </List>

      {/* Summary */}
      <Card sx={{ mt: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            History Summary
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                Total Queries
              </Typography>
              <Typography variant="h6">
                {state.queryHistory.length}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                Processed Queries
              </Typography>
              <Typography variant="h6">
                {state.queryHistory.filter(q => q.processed).length}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                Pending Queries
              </Typography>
              <Typography variant="h6">
                {state.queryHistory.filter(q => !q.processed).length}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                Latest Query
              </Typography>
              <Typography variant="h6">
                {state.queryHistory.length > 0 ? formatDate(state.queryHistory[0].created_at) : 'N/A'}
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
} 