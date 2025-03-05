# LimpehSays Telegram Bot

A Telegram bot that converts text to Singlish using DeepSeek via the OpenRouter API.

## Features

- Converts any text into Singlish using DeepSeek (via OpenRouter API)
- Works in group chats and responds only when mentioned (@LimpehSays text)
- Supports inline queries, allowing users to type @LimpehSays hello and get an instant Singlish translation
- Implements rate limiting to prevent spam
- Handles errors gracefully and logs issues for debugging
- Automatically switches between free and paid models if the free model fails

## Example Usage

- **Group Chat**: `@LimpehSays I am going to the store.`
  - Bot responds: "Limpeh go pasar liao, bo jio!"
  
- **Inline Query**: Type `@LimpehSays Hello, how are you?` in any chat
  - Bot provides a Singlish translation that you can send

## Setup

### Prerequisites

- Python 3.8 or higher (or Docker)
- A Telegram Bot Token (from [BotFather](https://t.me/botfather))
- An OpenRouter API key (from [OpenRouter](https://openrouter.ai/))

### Installation

#### Option 1: Standard Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/limpeh_says.git
   cd limpeh_says
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on the `.env.example` file:

   ```bash
   cp .env.example .env
   ```

5. Edit the `.env` file and add your Telegram Bot Token and OpenRouter API key:

   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   MODEL_TYPE=free  # Use 'free' for the free model or 'paid' for the paid model
   ```

#### Option 2: Docker Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/limpeh_says.git
   cd limpeh_says
   ```

2. Create a `.env` file based on the `.env.example` file:

   ```bash
   cp .env.example .env
   ```

3. Edit the `.env` file and add your Telegram Bot Token and OpenRouter API key:

   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   MODEL_TYPE=free  # Use 'free' for the free model or 'paid' for the paid model
   ```

4. Build and run the Docker container:

   ```bash
   docker-compose up -d
   ```

### Running the Bot

#### Standard Method

```bash
python bot.py
```

#### Docker Method

```bash
docker-compose up -d
```

## Deployment

### Option 1: Deploy on a VPS or Cloud Server

1. SSH into your server
2. Clone the repository and follow the installation steps above
3. Use a process manager like `systemd` or `supervisor` to keep the bot running

Example systemd service file (`/etc/systemd/system/limpehsays.service`):

```ini
[Unit]
Description=LimpehSays Telegram Bot
After=network.target

[Service]
User=yourusername
WorkingDirectory=/path/to/limpeh_says
ExecStart=/path/to/limpeh_says/venv/bin/python /path/to/limpeh_says/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable limpehsays
sudo systemctl start limpehsays
```

### Option 2: Deploy with Docker

1. SSH into your server
2. Clone the repository
3. Create and configure the `.env` file
4. Build and run the Docker container:

   ```bash
   docker-compose up -d
   ```

### Option 3: Deploy on Heroku

1. Create a `Procfile` in the project root:

   ```
   worker: python bot.py
   ```

2. Initialize a Git repository (if not already done):

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

3. Create a Heroku app and push to it:

   ```bash
   heroku create
   heroku config:set TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   heroku config:set OPENROUTER_API_KEY=your_openrouter_api_key_here
   heroku config:set MODEL_TYPE=free
   git push heroku main
   ```

4. Scale the worker dyno:

   ```bash
   heroku ps:scale worker=1
   ```

## Model Configuration

The bot can use either the free or paid DeepSeek model via OpenRouter:

- **Free Model**: `deepseek/deepseek-chat:free`
- **Paid Model**: `deepseek/deepseek-chat`

You can configure which model to use by setting the `MODEL_TYPE` environment variable in your `.env` file:

```
MODEL_TYPE=free  # Use the free model
```

or

```
MODEL_TYPE=paid  # Use the paid model
```

The bot is designed to automatically switch from the free model to the paid model if the free model fails (e.g., due to rate limiting). This behavior ensures that your bot continues to function even if the free model becomes unavailable.

## Customization

- To change the rate limit, modify the `RATE_LIMIT` value in your `.env` file
- To use a different model, modify the `model_name` property in the `config.py` file

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
