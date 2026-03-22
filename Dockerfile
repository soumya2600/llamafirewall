FROM python:3.11-slim

WORKDIR /app

# Copy backend code
COPY backend/ /app

# Install dependencies
RUN pip install --no-cache-dir \
    fastapi==0.109.2 \
    uvicorn==0.27.1 \
    pydantic==1.10.13 \
    python-dotenv==1.0.0 \
    httpx==0.27.0

# Start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
