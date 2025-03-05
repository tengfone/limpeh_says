FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set up logging directory with full permissions
RUN mkdir -p /app/logs && \
    chmod -R 777 /app

# Copy the rest of the application
COPY . .

# Ensure all files have proper permissions
RUN chmod -R 777 /app/logs && \
    touch /app/logs/bot.log && \
    chmod 666 /app/logs/bot.log

# Run the bot
CMD ["python", "bot.py"] 