from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from .infrastructure.logging_config import setup_logging
from .presentation.routes import query_router, insight_router, user_router, data_router

# Initialize logging
setup_logging()

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="GenAI Data Insights Platform",
    description="AI-powered business intelligence platform for retail analytics",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(query_router)
app.include_router(insight_router)
app.include_router(user_router)
app.include_router(data_router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "GenAI Data Insights Platform API", "status": "healthy", "hot_reload": "working"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
