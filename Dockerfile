FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a non-root user and set up logging
RUN useradd -m appuser && \
    mkdir -p logs && \
    touch logs/bot.log && \
    chown -R appuser:appuser logs && \
    chmod -R 755 logs

USER appuser

# Run the bot
CMD ["python", "bot.py"] 