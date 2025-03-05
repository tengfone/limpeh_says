FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user and group
RUN groupadd -r botgroup && \
    useradd -r -g botgroup -s /bin/false botuser

# Set up logging directory with proper permissions
RUN mkdir -p /app/logs && \
    chown botuser:botgroup /app/logs && \
    chmod 755 /app/logs

# Copy the rest of the application
COPY . .

# Set proper ownership
RUN chown -R botuser:botgroup /app

# Switch to non-root user
USER botuser

# Run the bot
CMD ["python", "bot.py"] 