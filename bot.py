"""
LimpehSays Telegram Bot

A Telegram bot that converts text to Singlish using OpenAI via OpenRouter API.
"""

import sys
import asyncio
import os
import logging
from logging.handlers import RotatingFileHandler
from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    InlineQueryHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters,
)
from telegram.constants import ParseMode

from config import config
from openrouter_client import OpenRouterClient
from rate_limiter import RateLimiter

# Configure logging
LOG_DIR = "logs"  # Changed from /app/logs to local logs directory
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_FILE = os.path.join(LOG_DIR, "limpehsays_log.log")

# Create logger
logger = logging.getLogger("LimpehSays")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

# File handler
try:
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=3,
        delay=True,  # Only create file when first record is written
    )
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
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
        "2. Mention me in a group chat (@LimpehSaysBot text)\n"
        "   ⚠️ Important: Grant me permission to read messages in groups!\n"
        "3. Use me inline in any chat by typing @LimpehSaysBot followed by text\n\n"
        "Try saying something to me! 🇸🇬"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    help_text = (
        "LimpehSays Bot Help\n\n"
        "I convert text to Singlish using AI. Here's how to use me:\n\n"
        "1. Direct chat: Just send me any message and I'll respond in Singlish\n"
        "2. In group chats: \n"
        "   • Mention me with @LimpehSaysBot Hello, how are you?\n"
        "   • ⚠️ Important: Make sure to grant me permission to read messages in the group!\n"
        "3. Inline mode: Type @LimpehSaysBot in any chat, followed by your text\n\n"
        "I have a rate limit to prevent spam. Please be patient if you hit the limit.\n\n"
        "🔗 GitHub: https://github.com/tengfone/limpeh_says"
    )
    await update.message.reply_text(help_text)


async def handle_direct_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle direct messages to the bot."""
    logger.info(
        f"Received direct message from user {update.effective_user.id}: {update.message.text if update.message else 'No text'}"
    )

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
        logger.info(f"Rate limited user {update.effective_user.id}")
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
        logger.info(
            f"Successfully translated for user {update.effective_user.id}: {update.message.text} -> {singlish_text}"
        )

        # Delete the processing message
        await processing_message.delete()

        # Reply with the translated text
        await update.message.reply_text(singlish_text)
    except Exception as e:
        logger.error(
            f"Error in direct message translation for user {update.effective_user.id}: {str(e)}"
        )
        # Delete the processing message
        await processing_message.delete()
        await update.message.reply_text(
            "Aiyo, sorry ah! Got problem with the translation. Try again later lah!"
        )


async def handle_mention(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle when the bot is mentioned in a message."""
    logger.info(f"[DEBUG] Entering handle_mention")

    if not update.message or not update.message.text:
        return

    # Only process messages that mention the bot
    if not update.message.entities:
        return

    bot_username = context.bot.username
    message_text = update.message.text
    is_mentioned = False
    mention_start = 0

    # Check for mentions in entities
    for entity in update.message.entities:
        if entity.type == "mention":
            mention = message_text[entity.offset : entity.offset + entity.length]
            if mention.lower() == f"@{bot_username}".lower():
                is_mentioned = True
                mention_start = entity.offset
                break

    if not is_mentioned:
        return

    # Extract text after the mention
    text = message_text[mention_start:].split(" ", 1)
    if len(text) < 2:
        await update.message.reply_text(
            "Tell me what to translate lah! Just type @LimpehSaysBot followed by your text.",
            reply_to_message_id=update.message.message_id,
        )
        return

    text = text[1].strip()
    logger.info(f"[DEBUG] Extracted text: {text}")

    # Check rate limiting
    if rate_limiter.is_rate_limited(update.effective_user.id):
        logger.info(f"Rate limited user {update.effective_user.id}")
        await update.message.reply_text(
            "Eh slow down lah! You sending too many messages. Wait a while can?",
            reply_to_message_id=update.message.message_id,
        )
        return

    # Send processing message
    processing_message = await update.message.reply_text(
        "Wait ah, limpeh thinking how to translate... 🤔",
        reply_to_message_id=update.message.message_id,
    )

    try:
        # Translate the text to Singlish
        singlish_text = await openrouter_client.translate_to_singlish(text)
        logger.info(
            f"Successfully translated mention for user {update.effective_user.id}: {text} -> {singlish_text}"
        )

        await processing_message.delete()
        await update.message.reply_text(
            singlish_text, reply_to_message_id=update.message.message_id
        )
    except Exception as e:
        logger.error(
            f"Error in mention translation for user {update.effective_user.id}: {str(e)}"
        )
        await processing_message.delete()
        await update.message.reply_text(
            "Aiyo, sorry ah! Got problem with the translation. Try again later lah!",
            reply_to_message_id=update.message.message_id,
        )


async def handle_inline_query(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle inline queries."""
    query = update.inline_query.query.strip()
    logger.info(
        f"[DEBUG] Received inline query from user {update.effective_user.id}. Query: '{query}'"
    )

    THUMBNAIL_URL = (
        "https://raw.githubusercontent.com/tengfone/limpeh_says/master/icon.jpeg"
    )

    try:
        if not query:
            # Simple prompt when no text is entered
            results = [
                InlineQueryResultArticle(
                    id="empty",
                    title="Enter text to translate",
                    description="Type your message...",
                    input_message_content=InputTextMessageContent(
                        "Please enter some text to translate"
                    ),
                    thumbnail_url=THUMBNAIL_URL,
                )
            ]
        else:
            # Show translate button without translating yet
            keyboard = [
                [
                    InlineKeyboardButton(
                        "🔄 Translate to Singlish", callback_data=f"translate:{query}"
                    )
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            results = [
                InlineQueryResultArticle(
                    id="translate_option",
                    title="Translate to Singlish",
                    description=query,
                    input_message_content=InputTextMessageContent(
                        f"🇬🇧 Text: {query}\n\n👇 Click below to translate!"
                    ),
                    reply_markup=reply_markup,
                    thumbnail_url=THUMBNAIL_URL,
                )
            ]

        await update.inline_query.answer(results, cache_time=0)
    except Exception as e:
        logger.error(f"[DEBUG] Error in inline query handler: {str(e)}", exc_info=True)
        try:
            error_results = [
                InlineQueryResultArticle(
                    id="error",
                    title="❌ Error",
                    description="Try again later",
                    input_message_content=InputTextMessageContent(
                        "System error! Try again later."
                    ),
                    thumbnail_url=THUMBNAIL_URL,
                )
            ]
            await update.inline_query.answer(error_results, cache_time=0)
        except Exception as answer_error:
            logger.error(f"[DEBUG] Could not send error message: {str(answer_error)}")


async def handle_callback_query(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle callback queries from inline buttons."""
    query = update.callback_query
    logger.info(f"Received callback query from user {query.from_user.id}: {query.data}")

    if not query.data.startswith("translate:"):
        await query.answer()
        return

    # Extract the text to translate
    text = query.data.split("translate:", 1)[1]

    # Check rate limiting
    if rate_limiter.is_rate_limited(query.from_user.id):
        logger.info(f"Rate limited callback query for user {query.from_user.id}")
        await query.answer("Eh slow down lah! Wait a while can?", show_alert=True)
        return

    # Show processing state
    await query.answer("Translating...")
    await query.edit_message_text(
        f"🇬🇧 Original: {text}\n\n🤔 Wait ah limpeh translating...",
    )

    try:
        # Translate the text
        singlish_text = await openrouter_client.translate_to_singlish(text)
        logger.info(
            f"Successfully translated callback query for user {query.from_user.id}: {text} -> {singlish_text}"
        )

        # Update with translation (without the "Translate Again" button)
        await query.edit_message_text(
            f"🇬🇧 Original: {text}\n🇸🇬 Singlish: {singlish_text}"
        )
    except Exception as e:
        logger.error(
            f"Error in callback query translation for user {query.from_user.id}: {str(e)}"
        )
        await query.edit_message_text(
            "Aiyo, cannot translate lah! Got problem with the system. Try again later!"
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in the dispatcher."""
    logger.error(f"Exception while handling an update: {context.error}")


def main() -> None:
    """Start the bot."""
    # Validate configuration
    try:
        config.validate_config()
    except ValueError as e:
        logger.error(f"Configuration config error: {str(e)}")
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

    # Handler for group messages (including mentions)
    application.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND
            & (filters.ChatType.GROUPS | filters.ChatType.SUPERGROUP),
            handle_mention,
            # Run this handler before others
            block=False,
        )
    )

    # Add inline query handler
    application.add_handler(InlineQueryHandler(handle_inline_query))

    # Add callback query handler
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    application.add_error_handler(error_handler)

    # Start the Bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
