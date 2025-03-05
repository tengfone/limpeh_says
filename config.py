"""Configuration module for the LimpehSays bot."""
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()

class Config(BaseModel):
    """Configuration model for the LimpehSays bot."""
    
    # Telegram Bot Token
    telegram_bot_token: str = Field(
        default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN", "")
    )
    
    # OpenRouter API Key
    openrouter_api_key: str = Field(
        default_factory=lambda: os.getenv("OPENROUTER_API_KEY", "")
    )
    
    # OpenRouter API URL
    openrouter_api_url: str = Field(
        default_factory=lambda: os.getenv(
            "OPENROUTER_API_URL", 
            "https://openrouter.ai/api/v1/chat/completions"
        )
    )
    
    # Rate limiting (requests per user per minute)
    rate_limit: int = Field(
        default_factory=lambda: int(os.getenv("RATE_LIMIT", "5"))
    )
    
    # Model configuration (free or paid)
    model_type: str = Field(
        default_factory=lambda: os.getenv("MODEL_TYPE", "free")
    )
    
    @property
    def model_name(self) -> str:
        """Get the model name based on the model type."""
        if self.model_type.lower() == "paid":
            return "deepseek/deepseek-chat"
        else:
            return "deepseek/deepseek-chat:free"
    
    def validate_config(self) -> bool:
        """Validate that all required configuration values are set."""
        if not self.telegram_bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set")
        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY is not set")
        return True


# Create a global config instance
config = Config() 