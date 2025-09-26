FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# Try main.py first, then start.py as fallback
CMD ["python", "main.py"]
