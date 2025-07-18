import React, { createContext, useContext, useReducer, ReactNode } from 'react';

// Types
export interface SalesDataItem {
  date: string;
  product: string;
  category: string;
  store: string;
  quantity: number;
  revenue: number;
  profit: number;
}

export interface InventoryDataItem {
  product: string;
  category: string;
  store: string;
  quantity: number;
  reorder_level: number;
  supplier: string;
}

export interface CustomerDataItem {
  customer_id: string;
  name: string;
  email: string;
  segment: string;
  total_purchases: number;
  last_purchase_date: string;
}

export interface BusinessMetrics {
  total_revenue: number;
  total_profit: number;
  profit_margin: number;
  total_customers: number;
  average_order_value: number;
  inventory_turnover: number;
}

export interface DataState {
  sales: SalesDataItem[];
  inventory: InventoryDataItem[];
  customers: CustomerDataItem[];
  metrics: BusinessMetrics | null;
  isLoading: boolean;
  error: string | null;
}

// Actions
type DataAction =
  | { type: 'SET_SALES_DATA'; payload: SalesDataItem[] }
  | { type: 'SET_INVENTORY_DATA'; payload: InventoryDataItem[] }
  | { type: 'SET_CUSTOMER_DATA'; payload: CustomerDataItem[] }
  | { type: 'SET_METRICS'; payload: BusinessMetrics }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'CLEAR_ERROR' };

// Initial state
const initialState: DataState = {
  sales: [],
  inventory: [],
  customers: [],
  metrics: null,
  isLoading: false,
  error: null,
};

// Reducer
function dataReducer(state: DataState, action: DataAction): DataState {
  switch (action.type) {
    case 'SET_SALES_DATA':
      return { ...state, sales: action.payload };
    case 'SET_INVENTORY_DATA':
      return { ...state, inventory: action.payload };
    case 'SET_CUSTOMER_DATA':
      return { ...state, customers: action.payload };
    case 'SET_METRICS':
      return { ...state, metrics: action.payload };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'CLEAR_ERROR':
      return { ...state, error: null };
    default:
      return state;
  }
}

// Context
interface DataContextType {
  state: DataState;
  dispatch: React.Dispatch<DataAction>;
}

const DataContext = createContext<DataContextType | undefined>(undefined);

// Provider
interface DataProviderProps {
  children: ReactNode;
}

export function DataProvider({ children }: DataProviderProps) {
  const [state, dispatch] = useReducer(dataReducer, initialState);

  return (
    <DataContext.Provider value={{ state, dispatch }}>
      {children}
    </DataContext.Provider>
  );
}

// Hook
export function useData() {
  const context = useContext(DataContext);
  if (context === undefined) {
    throw new Error('useData must be used within a DataProvider');
  }
  return context;
} 