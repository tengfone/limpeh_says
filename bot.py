"""
LimpehSays Telegram Bot

A Telegram bot that converts text to Singlish using OpenAI via OpenRouter API.
"""

import sys
import asyncio
import os
import logging
from logging.handlers import RotatingFileHandler
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    InlineQueryHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ParseMode

from config import config
from openrouter_client import OpenRouterClient
from rate_limiter import RateLimiter

# Configure logging
LOG_DIR = "/app/logs"
LOG_FILE = os.path.join(LOG_DIR, "limpehsays_log.log")

# Create logger
logger = logging.getLogger("LimpehSays")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

# File handler
try:
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=3,
        delay=True  # Only create file when first record is written
    )
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
except Exception as e:
    logger.warning(f"Could not set up file logging: {e}")

# Initialize clients
openrouter_client = OpenRouterClient()
rate_limiter = RateLimiter()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    await update.message.reply_text(
        "Hello! I am LimpehSays, a bot that converts text to Singlish.\n\n"
        "You can:\n"
        "1. Chat with me directly and I'll respond in Singlish\n"
        "2. Mention me in a group chat (@LimpehSays text)\n"
        "3. Use me inline by typing @LimpehSays followed by your text\n\n"
        "Try saying something to me!"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    help_text = (
        "LimpehSays Bot Help\n\n"
        "I convert text to Singlish using AI. Here's how to use me:\n\n"
        "1. Direct chat: Just send me any message and I'll respond in Singlish\n"
        "2. In group chats: Mention me with @LimpehSays Hello, how are you?\n"
        "3. Inline mode: Type @LimpehSays followed by your text in any chat\n\n"
        "I have a rate limit to prevent spam. Please be patient if you hit the limit.\n\n"
        "🔗 GitHub: https://github.com/tengfone/limpeh_says"
    )
    await update.message.reply_text(help_text)


async def handle_direct_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle direct messages to the bot."""
    # Check if message has text
    if not update.message or not update.message.text:
        await update.message.reply_text(
            "Eh bro, send me some text lah! Cannot translate empty message one!"
        )
        return

    # Ignore messages that are commands
    if update.message.text.startswith("/"):
        return

    # Check rate limiting
    if rate_limiter.is_rate_limited(update.effective_user.id):
        await update.message.reply_text(
            "Eh slow down lah! You sending too many messages. Wait a while can?"
        )
        return

    # Send processing message
    processing_message = await update.message.reply_text(
        "Wait ah, limpeh thinking how to translate... 🤔"
    )

    # Show typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    try:
        # Translate the text to Singlish
        singlish_text = await openrouter_client.translate_to_singlish(
            update.message.text
        )

        # Delete the processing message
        await processing_message.delete()

        # Reply with the translated text
        await update.message.reply_text(singlish_text)
    except Exception as e:
        logger.error(f"Error in direct message translation: {str(e)}")
        # Delete the processing message
        await processing_message.delete()
        await update.message.reply_text(
            "Aiyo, sorry ah! Got problem with the translation. Try again later lah!"
        )


async def handle_mention(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle when the bot is mentioned in a message."""
    # Check if this is a mention
    if not update.message or not update.message.text:
        return

    # Extract bot username
    bot_username = context.bot.username
    if f"@{bot_username}" not in update.message.text:
        return

    # Check rate limiting
    if rate_limiter.is_rate_limited(update.effective_user.id):
        await update.message.reply_text(
            "Eh slow down lah! You sending too many messages. Wait a while can?"
        )
        return

    # Extract the text after the mention
    text = update.message.text.split(f"@{bot_username}", 1)[1].strip()
    if not text:
        await update.message.reply_text(
            "Tell me what to translate lah! Just type @LimpehSays followed by your text."
        )
        return

    # Send processing message
    processing_message = await update.message.reply_text(
        "Wait ah, limpeh thinking how to translate... 🤔",
        reply_to_message_id=update.message.message_id,
    )

    # Show typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    try:
        # Translate the text to Singlish
        singlish_text = await openrouter_client.translate_to_singlish(text)

        # Delete the processing message
        await processing_message.delete()

        # Reply with the translated text
        await update.message.reply_text(
            singlish_text, reply_to_message_id=update.message.message_id
        )
    except Exception as e:
        logger.error(f"Error in mention translation: {str(e)}")
        # Delete the processing message
        await processing_message.delete()
        await update.message.reply_text(
            "Aiyo, sorry ah! Got problem with the translation. Try again later lah!",
            reply_to_message_id=update.message.message_id,
        )


async def handle_inline_query(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle inline queries."""
    query = update.inline_query.query

    if not query:
        # Show helpful message when no query is provided
        results = [
            InlineQueryResultArticle(
                id="empty",
                title="Type something to translate",
                description="Example: Hello, how are you?",
                input_message_content=InputTextMessageContent(
                    "Eh, type something after @LimpehSays lah! How to translate nothing?"
                ),
            )
        ]
        await update.inline_query.answer(results)
        return

    # Check rate limiting
    if rate_limiter.is_rate_limited(update.effective_user.id):
        results = [
            InlineQueryResultArticle(
                id="rate_limited",
                title="Rate Limited",
                description="You're sending too many requests. Please wait a moment.",
                input_message_content=InputTextMessageContent(
                    "Eh slow down lah! You sending too many messages. Wait a while can?"
                ),
            )
        ]
        await update.inline_query.answer(results)
        return

    # Show processing state
    processing_results = [
        InlineQueryResultArticle(
            id="processing",
            title="Translating...",
            description="Wait ah, limpeh thinking how to translate... 🤔",
            input_message_content=InputTextMessageContent("Processing translation..."),
        )
    ]
    await update.inline_query.answer(processing_results, cache_time=0)

    # Translate the text to Singlish
    try:
        singlish_text = await openrouter_client.translate_to_singlish(query)

        results = [
            InlineQueryResultArticle(
                id="1",
                title="Singlish Translation",
                description=singlish_text,
                input_message_content=InputTextMessageContent(
                    f"Original: {query}\nSinglish: {singlish_text}"
                ),
            )
        ]

        await update.inline_query.answer(results)
    except Exception as e:
        logger.error(f"Error handling inline query: {str(e)}")
        results = [
            InlineQueryResultArticle(
                id="error",
                title="Error",
                description="Something went wrong with the translation.",
                input_message_content=InputTextMessageContent(
                    "Aiyah, cannot translate lah! Got problem with the system."
                ),
            )
        ]
        await update.inline_query.answer(results)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in the dispatcher."""
    logger.error(f"Exception while handling an update: {context.error}")


def main() -> None:
    """Start the bot."""
    # Validate configuration
    try:
        config.validate_config()
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        sys.exit(1)

    # Create the Application
    application = Application.builder().token(config.telegram_bot_token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # Handler for direct messages (in private chats)
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,
            handle_direct_message,
        )
    )

    # Handler for mentions (in group chats)
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & ~filters.ChatType.PRIVATE, handle_mention
        )
    )

    # Handler for inline queries
    application.add_handler(InlineQueryHandler(handle_inline_query))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start the Bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
