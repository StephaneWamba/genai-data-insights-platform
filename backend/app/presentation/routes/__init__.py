from .query_routes import router as query_router
from .insight_routes import router as insight_router
from .user_routes import router as user_router
from .data_routes import router as data_router

__all__ = ["query_router", "insight_router", "user_router", "data_router"]
