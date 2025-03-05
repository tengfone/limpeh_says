FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a non-root user and set up permissions
RUN useradd -m appuser && \
    mkdir -p logs && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app

USER appuser

# Run the bot
CMD ["python", "bot.py"] 