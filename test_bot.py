"""Test script for the LimpehSays bot."""
import asyncio
from openrouter_client import OpenRouterClient
from config import config
from loguru import logger
import sys

# Configure logger
logger.remove()
logger.add(sys.stderr, level="INFO")


async def test_translation():
    """Test the translation functionality."""
    # Check if the OpenRouter API key is set
    if not config.openrouter_api_key:
        print("Error: OPENROUTER_API_KEY is not set in the .env file")
        return
    
    # Initialize the OpenRouter client
    client = OpenRouterClient()
    
    # Test phrases
    test_phrases = [
        "Hello, how are you?",
        "I am going to the store.",
        "This is a very interesting project.",
        "I can't believe it's already Friday!"
    ]
    
    # Test the translation
    for phrase in test_phrases:
        print(f"\nOriginal: {phrase}")
        try:
            singlish = await client.translate_to_singlish(phrase)
            print(f"Singlish: {singlish}")
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    print("Testing LimpehSays bot translation functionality...")
    print("Make sure you have set the OPENROUTER_API_KEY in the .env file")
    
    # Run the test
    asyncio.run(test_translation()) 