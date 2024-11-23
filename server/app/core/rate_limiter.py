from typing import Optional, Dict, Tuple
import time
from fastapi import HTTPException, Request
from app.core.config import settings

class RateLimiter:
    def __init__(self):
        # Store request timestamps for each user and endpoint
        # Format: {user_id: {endpoint: [(timestamp, tokens_used)]}}
        self._requests: Dict[int, Dict[str, list[Tuple[float, int]]]] = {}
        
        # Default rate limits
        self.WINDOW_SIZE = 3600  # 1 hour window
        self.DEFAULT_TOKENS = 1  # Default tokens per request
        self.MAX_TOKENS_PER_HOUR = 100  # Maximum tokens per hour
        
        # Token costs for different operations
        self.TOKEN_COSTS = {
            "/api/v1/ai/suggestions": 2,
            "/api/v1/ai/grammar": 1,
            "/api/v1/ai/citations": 2,
            "/api/v1/ai/tone": 2,
            "/api/v1/ai/research-questions": 3,
            "/api/v1/ai/outline": 3,
            "/api/v1/ai/literature-analysis": 4,
            "/api/v1/ai/methodology": 3,
            "/api/v1/ai/abstract": 3,
            "/api/v1/ai/keywords": 1,
            "/api/v1/ai/format-reference": 1,
            "/api/v1/ai/check-style": 2,
            "/api/v1/ai/extract-citations": 2,
            "/api/v1/ai/suggest-transitions": 2,
            "/api/v1/ai/check-arguments": 3,
            "/api/v1/ai/suggest-evidence": 2,
        }

    def _cleanup_old_requests(self, user_id: int, endpoint: str) -> None:
        """Remove requests older than the window size."""
        if user_id in self._requests and endpoint in self._requests[user_id]:
            current_time = time.time()
            self._requests[user_id][endpoint] = [
                req for req in self._requests[user_id][endpoint]
                if current_time - req[0] < self.WINDOW_SIZE
            ]

    def _get_tokens_used(self, user_id: int, endpoint: str) -> int:
        """Calculate total tokens used in current window."""
        if user_id not in self._requests or endpoint not in self._requests[user_id]:
            return 0
        
        current_time = time.time()
        return sum(
            tokens for timestamp, tokens in self._requests[user_id][endpoint]
            if current_time - timestamp < self.WINDOW_SIZE
        )

    def _get_token_cost(self, endpoint: str) -> int:
        """Get token cost for an endpoint."""
        return self.TOKEN_COSTS.get(endpoint, self.DEFAULT_TOKENS)

    def check_rate_limit(self, request: Request, user_id: int) -> None:
        """
        Check if the request is within rate limits.
        Raises HTTPException if rate limit is exceeded.
        """
        endpoint = request.url.path
        
        # Initialize user's request history if needed
        if user_id not in self._requests:
            self._requests[user_id] = {}
        if endpoint not in self._requests[user_id]:
            self._requests[user_id][endpoint] = []

        # Clean up old requests
        self._cleanup_old_requests(user_id, endpoint)

        # Calculate tokens needed and used
        tokens_needed = self._get_token_cost(endpoint)
        tokens_used = self._get_tokens_used(user_id, endpoint)

        # Check if adding this request would exceed the limit
        if tokens_used + tokens_needed > self.MAX_TOKENS_PER_HOUR:
            remaining_time = self._get_reset_time(user_id, endpoint)
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate limit exceeded",
                    "reset_in_seconds": remaining_time,
                    "tokens_used": tokens_used,
                    "tokens_limit": self.MAX_TOKENS_PER_HOUR
                }
            )

        # Record the request
        current_time = time.time()
        self._requests[user_id][endpoint].append((current_time, tokens_needed))

    def _get_reset_time(self, user_id: int, endpoint: str) -> int:
        """Calculate time until rate limit resets."""
        if not self._requests[user_id][endpoint]:
            return 0
        
        oldest_request = min(req[0] for req in self._requests[user_id][endpoint])
        return int(oldest_request + self.WINDOW_SIZE - time.time())

    def get_rate_limit_info(self, user_id: int, endpoint: str) -> Dict:
        """Get current rate limit information for a user and endpoint."""
        self._cleanup_old_requests(user_id, endpoint)
        tokens_used = self._get_tokens_used(user_id, endpoint)
        reset_time = self._get_reset_time(user_id, endpoint)
        
        return {
            "tokens_used": tokens_used,
            "tokens_remaining": self.MAX_TOKENS_PER_HOUR - tokens_used,
            "reset_in_seconds": reset_time
        }

# Global rate limiter instance
rate_limiter = RateLimiter()