FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

EXPOSE $PORT

# Run uvicorn with dynamic port
CMD ["sh", "-c", "python -m uvicorn mcp_ui_aggregator.api.app:app --host 0.0.0.0 --port $PORT"]
