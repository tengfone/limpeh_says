"""Rate limiting functionality for the bot."""
import time
import logging
from config import config

# Get logger for this module
logger = logging.getLogger(__name__)

class RateLimiter:
    """Rate limiting implementation."""

    def __init__(self):
        """Initialize the rate limiter."""
        self.requests = {}  # user_id -> list of timestamps
        self.rate_limit = config.rate_limit  # requests per minute

    def is_rate_limited(self, user_id: int) -> bool:
        """
        Check if a user has exceeded their rate limit.
        
        Args:
            user_id: The Telegram user ID to check
            
        Returns:
            True if the user has exceeded their rate limit, False otherwise
        """
        current_time = time.time()
        
        # Get the user's request history
        user_requests = self.requests.get(user_id, [])
        
        # Remove requests older than 1 minute
        user_requests = [t for t in user_requests if current_time - t < 60]
        
        # Update the requests list
        self.requests[user_id] = user_requests
        
        # Check if the user has exceeded their rate limit
        if len(user_requests) >= self.rate_limit:
            logger.warning(f"User {user_id} exceeded rate limit")
            return True
            
        # Add the current request
        user_requests.append(current_time)
        return False 