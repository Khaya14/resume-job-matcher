# =================================================================
# resume-job-matcher – FastAPI backend Dockerfile (Member 3)
# Multi-stage → tiny, secure, professional image
# =================================================================

# Stage 1: Install dependencies
FROM python:3.12-slim AS builder
WORKDIR /app

# Copy requirements first (caching magic)
COPY ../backend/requirements.txt .                     
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Final tiny image
FROM python:3.12-slim

# Create non-root user (security!)
RUN adduser --disabled-password --gecos '' appuser
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy only the backend code we need
COPY ../backend/ .                                    

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]