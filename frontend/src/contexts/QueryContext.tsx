import React, { createContext, useContext, useReducer, ReactNode } from 'react';

// Types
export interface QueryInfo {
  id: number;
  text: string;
  user_id?: string;
  processed: boolean;
  response?: string;
  created_at: string;
}

export interface InsightResponse {
  title: string;
  description: string;
  category: string;
  confidence_score: number;
  data_sources: string[];
}

export interface VisualizationResponse {
  type: string;
  title: string;
  data_source: string;
  chart_data?: any; // Chart.js configuration data
  data_points?: number;
  columns_used?: string[];
}

export interface QueryResponse {
  success: boolean;
  query: QueryInfo;
  intent: Record<string, any>;
  insights: InsightResponse[];
  recommendations: string[];
  visualizations: VisualizationResponse[];
  processed_at: string;
}

export interface QueryState {
  currentQuery: string;
  queryHistory: QueryInfo[];
  currentResponse: QueryResponse | null;
  isLoading: boolean;
  error: string | null;
}

// Actions
type QueryAction =
  | { type: 'SET_CURRENT_QUERY'; payload: string }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_RESPONSE'; payload: QueryResponse }
  | { type: 'ADD_TO_HISTORY'; payload: QueryInfo }
  | { type: 'CLEAR_ERROR' };

// Initial state
const initialState: QueryState = {
  currentQuery: '',
  queryHistory: [],
  currentResponse: null,
  isLoading: false,
  error: null,
};

// Reducer
function queryReducer(state: QueryState, action: QueryAction): QueryState {
  switch (action.type) {
    case 'SET_CURRENT_QUERY':
      return { ...state, currentQuery: action.payload };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'SET_RESPONSE':
      return { ...state, currentResponse: action.payload, error: null };
    case 'ADD_TO_HISTORY':
      return {
        ...state,
        queryHistory: [action.payload, ...state.queryHistory],
      };
    case 'CLEAR_ERROR':
      return { ...state, error: null };
    default:
      return state;
  }
}

// Context
interface QueryContextType {
  state: QueryState;
  dispatch: React.Dispatch<QueryAction>;
}

const QueryContext = createContext<QueryContextType | undefined>(undefined);

// Provider
interface QueryProviderProps {
  children: ReactNode;
}

export function QueryProvider({ children }: QueryProviderProps) {
  const [state, dispatch] = useReducer(queryReducer, initialState);

  return (
    <QueryContext.Provider value={{ state, dispatch }}>
      {children}
    </QueryContext.Provider>
  );
}

// Hook
export function useQuery() {
  const context = useContext(QueryContext);
  if (context === undefined) {
    throw new Error('useQuery must be used within a QueryProvider');
  }
  return context;
} 