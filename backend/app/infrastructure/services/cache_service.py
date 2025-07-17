import logging
import json
import redis
from typing import Optional, Any, Dict
from datetime import datetime, timedelta
import os

logger = logging.getLogger("cache_service")


class CacheService:
    """
    Redis-based caching service for query results and insights.
    Implements caching strategies for performance optimization.
    """

    def __init__(self):
        """Initialize Redis connection and cache configuration"""
        try:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
            self.redis_client = redis.from_url(
                redis_url, decode_responses=True)
            self.redis_client.ping()  # Test connection
            logger.info("Redis cache connection established")
        except Exception as e:
            logger.warning(
                f"Redis connection failed: {e}. Cache will be disabled.")
            self.redis_client = None

        # Cache configuration
        self.default_ttl = 3600  # 1 hour default
        self.query_cache_ttl = 1800  # 30 minutes for query results
        self.insight_cache_ttl = 7200  # 2 hours for insights

    def _generate_cache_key(self, prefix: str, identifier: str) -> str:
        """Generate a standardized cache key"""
        return f"genai:{prefix}:{identifier}"

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        if not self.redis_client:
            return None

        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    def set(self, key: str, value: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """
        Store value in cache

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds

        Returns:
            True if successful, False otherwise
        """
        if not self.redis_client:
            return False

        try:
            ttl = ttl or self.default_ttl
            serialized_value = json.dumps(value, default=str)
            self.redis_client.setex(key, ttl, serialized_value)
            logger.debug(f"Cached value for key: {key}")
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """
        Delete value from cache

        Args:
            key: Cache key

        Returns:
            True if successful, False otherwise
        """
        if not self.redis_client:
            return False

        try:
            self.redis_client.delete(key)
            logger.debug(f"Deleted cache key: {key}")
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False

    def cache_query_result(self, query_id: int, result: Dict[str, Any]) -> bool:
        """
        Cache query processing result

        Args:
            query_id: Query identifier
            result: Query result to cache

        Returns:
            True if cached successfully
        """
        key = self._generate_cache_key("query_result", str(query_id))
        return self.set(key, result, self.query_cache_ttl)

    def get_cached_query_result(self, query_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached query result

        Args:
            query_id: Query identifier

        Returns:
            Cached query result or None
        """
        key = self._generate_cache_key("query_result", str(query_id))
        return self.get(key)

    def cache_insights(self, query_id: int, insights: list) -> bool:
        """
        Cache insights for a query

        Args:
            query_id: Query identifier
            insights: List of insights to cache

        Returns:
            True if cached successfully
        """
        key = self._generate_cache_key("insights", str(query_id))
        return self.set(key, {"insights": insights}, self.insight_cache_ttl)

    def get_cached_insights(self, query_id: int) -> Optional[list]:
        """
        Retrieve cached insights

        Args:
            query_id: Query identifier

        Returns:
            Cached insights or None
        """
        key = self._generate_cache_key("insights", str(query_id))
        cached_data = self.get(key)
        return cached_data.get("insights") if cached_data else None

    def cache_intent_analysis(self, query_text: str, intent: Dict[str, Any]) -> bool:
        """
        Cache intent analysis for similar queries

        Args:
            query_text: Original query text
            intent: Intent analysis result

        Returns:
            True if cached successfully
        """
        # Use hash of query text as identifier for similar queries
        import hashlib
        query_hash = hashlib.md5(query_text.encode()).hexdigest()
        key = self._generate_cache_key("intent", query_hash)
        return self.set(key, intent, self.query_cache_ttl)

    def get_cached_intent_analysis(self, query_text: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached intent analysis

        Args:
            query_text: Original query text

        Returns:
            Cached intent analysis or None
        """
        import hashlib
        query_hash = hashlib.md5(query_text.encode()).hexdigest()
        key = self._generate_cache_key("intent", query_hash)
        return self.get(key)

    def invalidate_query_cache(self, query_id: int) -> bool:
        """
        Invalidate all cache entries for a specific query

        Args:
            query_id: Query identifier

        Returns:
            True if successful
        """
        success = True
        success &= self.delete(self._generate_cache_key(
            "query_result", str(query_id)))
        success &= self.delete(
            self._generate_cache_key("insights", str(query_id)))
        return success

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics

        Returns:
            Dictionary with cache statistics
        """
        if not self.redis_client:
            return {"status": "disabled", "message": "Redis not available"}

        try:
            info = self.redis_client.info()
            return {
                "status": "active",
                "total_connections_received": info.get("total_connections_received", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "used_memory_human": info.get("used_memory_human", "0B"),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0)
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"status": "error", "message": str(e)}
