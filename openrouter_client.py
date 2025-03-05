"""OpenRouter API client for translating text to Singlish."""
import httpx
import logging
from config import config

# Get logger for this module
logger = logging.getLogger(__name__)

class OpenRouterClient:
    """Client for interacting with the OpenRouter API to translate text to Singlish."""

    def __init__(self):
        """Initialize the OpenRouter client with configuration."""
        self.api_key = config.openrouter_api_key
        self.api_url = config.openrouter_api_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/yourusername/limpeh_says",  # Update with your repo
            "X-Title": "LimpehSays Telegram Bot"
        }
        self.free_model_failed = False

    async def translate_to_singlish(self, text: str) -> str:
        """
        Translate the given text to Singlish using DeepSeek via OpenRouter.
        
        Args:
            text: The text to translate to Singlish
            
        Returns:
            The translated Singlish text
            
        Raises:
            Exception: If there's an error communicating with the OpenRouter API
        """
        # Log the input text
        logger.info(f"Received text to translate: {text}")
        
        try:
            # Determine which model to use
            model_name = config.model_name
            
            # If the free model has failed before and we're still configured to use it,
            # switch to the paid model
            if self.free_model_failed and model_name == "deepseek/deepseek-chat:free":
                logger.warning("Free model previously failed, switching to paid model")
                model_name = "deepseek/deepseek-chat"
            
            # Prepare the system prompt and user prompt
            system_prompt = "You are a Singaporean who speaks Singlish fluently. Translate text to authentic Singlish using common particles (lah, leh, lor, ah, sia), local expressions, and proper Singlish grammar. Keep responses short and natural."
            
            user_prompt = f"Convert this to Singlish (keep it short and natural): {text}"
            
            # Prepare the request payload
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.5,  # Lower temperature for more consistent output
                "max_tokens": 100  # Reduced max tokens since we want concise responses
            }
            
            logger.info(f"Using model: {model_name}")
            
            # Make the API request
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload
                )
                
                # Check if the request was successful
                response.raise_for_status()
                response_data = response.json()
                
                # Extract the translated text from the response
                translated_text = response_data["choices"][0]["message"]["content"].strip()
                logger.info(f"Translation: '{text}' → '{translated_text}'")
                return translated_text
                
        except Exception as e:
            logger.error(f"Error translating text: '{text}'. Error: {str(e)}")
            
            # If we're using the free model and it failed, mark it as failed and try the paid model
            if config.model_name == "deepseek/deepseek-chat:free" and not self.free_model_failed:
                self.free_model_failed = True
                logger.warning("Free model failed, trying paid model")
                try:
                    return await self.translate_to_singlish(text)
                except Exception as e2:
                    logger.error(f"Paid model also failed: {str(e2)}")
            
            # Return a fallback message in case of error
            return f"Aiyah, cannot translate lah! Got problem: {str(e)}" 