# 🇸🇬 LimpehSays Telegram Bot

<div align="center">

![LimpehSays Logo](icon.jpeg)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://t.me/LimpehSaysBot)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)

*Your friendly Singlish translator bot for Telegram! Convert any English text to authentic Singaporean English (Singlish).*

[Add to Telegram](https://t.me/LimpehSaysBot) • [Report Bug](https://github.com/tengfone/limpeh_says/issues) • [Request Feature](https://github.com/tengfone/limpeh_says/issues)

</div>

---

## 🤖 About The Bot

LimpehSays is a Telegram bot that converts English text to authentic Singlish using DeepSeek AI via OpenRouter. Whether you want to sound more local or just have fun with Singlish, this bot has got you covered!

### 🌟 Features

- 🗣️ **Direct Chat Translation**: Chat directly with the bot to get instant Singlish translations
- 👥 **Group Chat Support**: Add to groups and mention `@LimpehSays` for translations
- 🔄 **Smart Model Switching**: Automatically switches between free and paid models
- 🛡️ **Rate Limiting**: Prevents spam and ensures fair usage
- 📝 **Comprehensive Logging**: Tracks translations and errors for debugging
- 🔄 **Inline Mode**: Use the bot in any chat by typing `@LimpehSays` followed by your text

### 💬 Usage Examples

```
You: I am going to the store
Bot: Going pasar ah!

You: This food is very delicious
Bot: Wah the food damn shiok sia!

You: I don't understand what you're saying
Bot: Dun understand leh, say what?
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher (or Docker)
- Telegram Bot Token (from [BotFather](https://t.me/botfather))
- OpenRouter API key (from [OpenRouter](https://openrouter.ai/))

### 🐳 Docker Installation (Recommended)

1. Clone the repository:

   ```bash
   git clone https://github.com/tengfone/limpeh_says.git
   cd limpeh_says
   ```

2. Create and configure `.env`:

   ```bash
   cp .env.example .env
   # Edit .env with your tokens
   ```

3. Build and run:

   ```bash
   docker-compose up -d
   ```

### 🐍 Standard Installation

1. Clone and setup virtual environment:

   ```bash
   git clone https://github.com/tengfone/limpeh_says.git
   cd limpeh_says
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:

   ```bash
   cp .env.example .env
   # Edit .env with your tokens
   ```

4. Run the bot:

   ```bash
   python bot.py
   ```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | Required |
| `OPENROUTER_API_KEY` | OpenRouter API key | Required |
| `RATE_LIMIT` | Requests per user per minute | 5 |
| `MODEL_TYPE` | AI model type ('free' or 'paid') | free |
| `OPENROUTER_API_URL` | OpenRouter API URL | Required |

### AI Models

- **Free Model**: `deepseek/deepseek-chat:free`
- **Paid Model**: `deepseek/deepseek-chat`

## 🌐 Deployment

The recommended way to deploy LimpehSays is using Docker on a VPS or cloud server.

1. SSH into your server
2. Clone the repository
3. Create and configure the `.env` file
4. Run the deployment script:

   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

The deployment script will:

- Check for required configuration
- Pull the latest changes
- Build and start the Docker container
- Set up automatic restarts
- Provide commands for viewing logs and managing the bot

## 📝 Logging

The bot maintains detailed logs in `bot.log`:

- Input text logging
- Translation results
- Error tracking
- Model usage monitoring

View logs in real-time:

```bash
tail -f bot.log
```

## 🛠️ Development

### Project Structure

```
limpeh_says/
├── bot.py              # Main bot logic
├── config.py           # Configuration handling
├── openrouter_client.py # API client
├── rate_limiter.py     # Rate limiting logic
├── requirements.txt    # Dependencies
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose config
└── deploy.sh          # Deployment script
```

### Running Tests

```bash
python test_bot.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👏 Acknowledgments

- [python-telegram-bot](https://python-telegram-bot.org/) for the amazing Telegram bot framework
- [OpenRouter](https://openrouter.ai/) for providing AI model access
- [DeepSeek](https://deepseek.com/) for the language models

---

<div align="center">
Made with ❤️ in Singapore 🇸🇬
</div>
