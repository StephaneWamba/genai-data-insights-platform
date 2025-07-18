# GenAI Data Insights Platform - Frontend

## Overview

This is the frontend application for the GenAI Data Insights Platform, a React-based dashboard that provides natural language query capabilities and data visualization for business analytics.

## Features

### 🎯 Core Features

- **Natural Language Query Interface**: Ask business questions in plain English
- **AI-Powered Insights**: Get automated insights and recommendations
- **Real-time Data Visualization**: View sales, inventory, and customer data
- **Business Metrics Dashboard**: Key performance indicators at a glance
- **Query History**: Track and review past queries and insights
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### 🏗️ Architecture

- **React 18** with TypeScript for type safety
- **Material-UI (MUI)** for modern, accessible UI components
- **Context API** for state management
- **Axios** for API communication
- **Clean Architecture** with separation of concerns

## Project Structure

```
src/
├── components/           # React components
│   ├── Dashboard.tsx     # Main dashboard layout
│   ├── QueryInterface.tsx # Natural language query interface
│   ├── BusinessMetrics.tsx # Business metrics display
│   ├── DataVisualization.tsx # Data tables and charts
│   └── QueryHistory.tsx  # Query history and insights
├── contexts/            # React contexts for state management
│   ├── QueryContext.tsx # Query state and history
│   └── DataContext.tsx  # Data state management
├── services/            # API services
│   └── api.ts          # HTTP client and API endpoints
├── App.tsx             # Main application component
└── index.tsx           # Application entry point
```

## Getting Started

### Prerequisites

- Node.js 16+
- npm or yarn
- Backend API running on `http://localhost:8000`

### Installation

1. **Install dependencies**:

   ```bash
   npm install
   ```

2. **Start the development server**:

   ```bash
   npm start
   ```

3. **Open your browser**:
   Navigate to `http://localhost:3000`

### Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

## API Integration

The frontend integrates with the following backend endpoints:

### Query Processing

- `POST /api/v1/queries/process` - Process natural language queries
- `GET /api/v1/queries/{id}` - Get query by ID
- `GET /api/v1/queries/health` - Health check

### Data Endpoints

- `GET /api/v1/data/sales` - Sales data
- `GET /api/v1/data/inventory` - Inventory data
- `GET /api/v1/data/customers` - Customer data
- `GET /api/v1/data/metrics` - Business metrics
- `GET /api/v1/data/search` - Search data

### Insights

- `GET /api/v1/insights/{id}` - Get insight by ID
- `GET /api/v1/insights/query/{queryId}` - Get insights by query
- `GET /api/v1/insights/category/{category}` - Get insights by category

## Component Documentation

### Dashboard

The main dashboard component with navigation and layout management.

**Features:**

- Responsive sidebar navigation
- Mobile-friendly drawer
- Dynamic content rendering
- Theme integration

### QueryInterface

Natural language query processing interface.

**Features:**

- Multi-line text input
- Query suggestions
- Real-time processing feedback
- Structured response display
- Intent analysis visualization
- AI insights presentation
- Actionable recommendations

### BusinessMetrics

Business performance metrics dashboard.

**Features:**

- Key performance indicators
- Real-time data display
- Color-coded status indicators
- Performance summaries
- Currency and number formatting

### DataVisualization

Data tables and analytics display.

**Features:**

- Sortable data tables
- Search and filtering
- Pagination
- Summary statistics
- Multiple data type support (sales, inventory, customers)

### QueryHistory

Query history and insights tracking.

**Features:**

- Historical query display
- Detailed insight review
- Confidence scoring
- Recommendation tracking
- Summary statistics

## State Management

### QueryContext

Manages query-related state:

- Current query text
- Query history
- Processing status
- Error handling
- Response data

### DataContext

Manages data-related state:

- Sales data
- Inventory data
- Customer data
- Business metrics
- Loading states
- Error handling

## Styling and Theming

The application uses Material-UI with a custom theme:

- **Primary Color**: Blue (#1976d2)
- **Secondary Color**: Pink (#dc004e)
- **Background**: Light gray (#f5f5f5)
- **Cards**: Rounded corners with subtle shadows
- **Typography**: Custom font weights and sizes

## Performance Optimizations

- **Lazy Loading**: Components load on demand
- **Memoization**: React.memo for expensive components
- **Debounced Search**: Search input optimization
- **Pagination**: Large datasets handled efficiently
- **Error Boundaries**: Graceful error handling

## Accessibility

- **ARIA Labels**: Proper accessibility attributes
- **Keyboard Navigation**: Full keyboard support
- **Screen Reader**: Compatible with assistive technologies
- **Color Contrast**: WCAG compliant color schemes
- **Focus Management**: Proper focus indicators

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Development

### Available Scripts

```bash
npm start          # Start development server
npm run build      # Build for production
npm test           # Run tests
npm run eject      # Eject from Create React App
```

### Code Style

- **TypeScript**: Strict mode enabled
- **ESLint**: Code quality enforcement
- **Prettier**: Code formatting
- **Component Structure**: Functional components with hooks
- **File Naming**: PascalCase for components, camelCase for utilities

## Deployment

### Production Build

```bash
npm run build
```

The build output will be in the `build/` directory.

### Docker Deployment

```bash
docker build -t genai-frontend .
docker run -p 3000:3000 genai-frontend
```

## Troubleshooting

### Common Issues

1. **API Connection Errors**

   - Verify backend is running on port 8000
   - Check CORS configuration
   - Validate API endpoints

2. **Build Errors**

   - Clear node_modules and reinstall
   - Check TypeScript compilation
   - Verify dependency versions

3. **Performance Issues**
   - Check network tab for slow requests
   - Monitor component re-renders
   - Verify data pagination

## Contributing

1. Follow the existing code style
2. Add TypeScript types for new features
3. Include error handling
4. Test on multiple screen sizes
5. Update documentation

## License

This project is part of the GenAI Data Insights Platform.
