FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl zstd sed && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set up the working directory
WORKDIR /app

# Copy requirements first and install your dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Copy the rest of your application files
COPY . /app

# Create a clean startup script to handle both Ollama and your app
RUN echo '#!/bin/bash' > /app/start.sh && \
    echo 'ollama serve > /dev/null 2>&1 &' >> /app/start.sh && \
    echo 'sleep 5' >> /app/start.sh && \
    echo 'ollama pull llama3.2 > /dev/null 2>&1' >> /app/start.sh && \
    echo 'python3 app.py' >> /app/start.sh

# Fix Windows line endings and make script executable
RUN sed -i 's/\r$//' /app/start.sh && chmod +x /app/start.sh

ENV OLLAMA_HOST=0.0.0.0

# Start everything via the script
ENTRYPOINT ["/app/start.sh"]