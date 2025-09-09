# Use official Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app


# Install dependencies
RUN pip install .

# Expose port (change if your MCP server uses a different port)
EXPOSE 8000

# Start all servers (adjust the script name if needed)
CMD ["python", "server/all_servers.py"]
