# Dockerfile
FROM python:3.9-slim
WORKDIR /app

# Copy dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port (Heroku assigns a PORT dynamically via environment variable)
EXPOSE $PORT

# Command to run your lobby server (or combined server if applicable)
CMD ["python", "lobby_server.py"]
