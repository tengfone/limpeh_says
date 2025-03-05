"""Rate limiter module to prevent spam."""
import time
from collections import defaultdict
from loguru import logger
from config import config


class RateLimiter:
    """Rate limiter to prevent spam by limiting requests per user."""
    
    def __init__(self):
        """Initialize the rate limiter with configuration."""
        self.rate_limit = config.rate_limit
        self.window_size = 60  # 1 minute window
        self.user_requests = defaultdict(list)
        
    def is_rate_limited(self, user_id: int) -> bool:
        """
        Check if a user is rate limited.
        
        Args:
            user_id: The Telegram user ID
            
        Returns:
            True if the user is rate limited, False otherwise
        """
        current_time = time.time()
        user_requests = self.user_requests[user_id]
        
        # Remove requests older than the window size
        self.user_requests[user_id] = [
            req_time for req_time in user_requests 
            if current_time - req_time < self.window_size
        ]
        
        # Check if the user has exceeded the rate limit
        if len(self.user_requests[user_id]) >= self.rate_limit:
            logger.warning(f"User {user_id} is rate limited")
            return True
        
        # Add the current request
        self.user_requests[user_id].append(current_time)
        return False 