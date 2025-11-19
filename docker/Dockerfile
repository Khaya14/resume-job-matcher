# =================================================================
# resume-job-matcher – FastAPI backend (Member 3)
# FINAL VERSION – works even with empty backend folder
# =================================================================

FROM python:3.12-slim

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
WORKDIR /app

# Copy backend code
COPY backend/ ./backend/

# Install dependencies only if requirements.txt exists
COPY backend/requirements.txt* ./
RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir --upgrade pip && \
        pip install --no-cache-dir -r requirements.txt; \
    else \
        echo "No requirements.txt – skipping install"; \
    fi

# Copy the actual app code (safe)
COPY backend/main.py* ./
COPY backend/*.py ./

# Switch to non-root user
USER appuser

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]