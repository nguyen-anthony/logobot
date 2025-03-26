# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directory for logos
RUN mkdir -p logos

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "logo_cycler.py"] 