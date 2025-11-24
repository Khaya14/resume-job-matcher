# Dockerfile — FINAL VERSION (serves frontend + backend)
FROM python:3.11-slim

# Install nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./backend/

# Copy frontend (HTML) to nginx
COPY frontend/ /usr/share/nginx/html/

# Custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

# Start both nginx + FastAPI
CMD service nginx start && python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000