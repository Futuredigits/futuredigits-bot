# Use official Python 3.10 image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Default environment variable (will be overwritten in Render)
ENV BOT_TOKEN=REPLACE_ME

# Start the bot
CMD ["python", "bot.py"]
