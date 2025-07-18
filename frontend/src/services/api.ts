import axios, { AxiosResponse } from 'axios';
import { QueryResponse } from '../contexts/QueryContext';
import { 
  SalesDataItem, 
  InventoryDataItem, 
  CustomerDataItem, 
  BusinessMetrics 
} from '../contexts/DataContext';

// API base configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Query API
export const queryAPI = {
  /**
   * Process a natural language query and return AI-generated insights
   * @param queryText - The natural language query
   * @param userId - Optional user identifier
   * @returns Promise with query response including insights and recommendations
   */
  processQuery: async (queryText: string, userId?: string): Promise<QueryResponse> => {
    const response: AxiosResponse<QueryResponse> = await api.post('/api/v1/queries/process', {
      query_text: queryText,
      user_id: userId,
    });
    return response.data;
  },

  /**
   * Get query by ID
   * @param queryId - The query ID
   * @returns Promise with query details
   */
  getQuery: async (queryId: number): Promise<any> => {
    const response = await api.get(`/api/v1/queries/${queryId}`);
    return response.data;
  },

  /**
   * Health check for query service
   * @returns Promise with service health status
   */
  healthCheck: async (): Promise<any> => {
    const response = await api.get('/api/v1/queries/health');
    return response.data;
  },
};

// Data API
export const dataAPI = {
  /**
   * Get sales data for analysis
   * @param days - Number of days of data to retrieve (default: 30)
   * @returns Promise with sales data
   */
  getSalesData: async (days: number = 30): Promise<SalesDataItem[]> => {
    const response = await api.get(`/api/v1/data/sales?days=${days}`);
    return response.data.data;
  },

  /**
   * Get inventory data for analysis
   * @returns Promise with inventory data
   */
  getInventoryData: async (): Promise<InventoryDataItem[]> => {
    const response = await api.get('/api/v1/data/inventory');
    return response.data.data;
  },

  /**
   * Get customer data for analysis
   * @param count - Number of customers to retrieve (default: 100)
   * @returns Promise with customer data
   */
  getCustomerData: async (count: number = 100): Promise<CustomerDataItem[]> => {
    const response = await api.get(`/api/v1/data/customers?count=${count}`);
    return response.data.data;
  },

  /**
   * Get business metrics and performance data
   * @returns Promise with business metrics
   */
  getBusinessMetrics: async (): Promise<BusinessMetrics> => {
    const response = await api.get('/api/v1/data/metrics');
    return response.data.data;
  },

  /**
   * Search data based on natural language query
   * @param query - Natural language search query
   * @returns Promise with relevant data
   */
  searchData: async (query: string): Promise<any> => {
    const response = await api.get(`/api/v1/data/search?query=${encodeURIComponent(query)}`);
    return response.data;
  },

  /**
   * Health check for data service
   * @returns Promise with service health status
   */
  healthCheck: async (): Promise<any> => {
    const response = await api.get('/api/v1/data/health');
    return response.data;
  },
};

// Insights API
export const insightsAPI = {
  /**
   * Get insight by ID
   * @param insightId - The insight ID
   * @returns Promise with insight details
   */
  getInsight: async (insightId: number): Promise<any> => {
    const response = await api.get(`/api/v1/insights/${insightId}`);
    return response.data;
  },

  /**
   * Get insights by query ID
   * @param queryId - The query ID
   * @returns Promise with insights for the query
   */
  getInsightsByQuery: async (queryId: number): Promise<any> => {
    const response = await api.get(`/api/v1/insights/query/${queryId}`);
    return response.data;
  },

  /**
   * Get insights by category
   * @param category - The insight category
   * @returns Promise with insights for the category
   */
  getInsightsByCategory: async (category: string): Promise<any> => {
    const response = await api.get(`/api/v1/insights/category/${category}`);
    return response.data;
  },

  /**
   * Health check for insights service
   * @returns Promise with service health status
   */
  healthCheck: async (): Promise<any> => {
    const response = await api.get('/api/v1/insights/health');
    return response.data;
  },
};

export default api; 