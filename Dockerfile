# Multi-stage Dockerfile for unified deployment on Railway, Render, or Docker
# Stage 1: Build React/Vite Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# Stage 2: FastAPI Backend with Embedded Frontend
FROM python:3.11-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Python requirements
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend, documentation, and app metadata
COPY backend/ ./backend/
COPY docs/ ./docs/
COPY AGENTS.md ./

# Copy compiled frontend from Stage 1 into backend static
COPY --from=frontend-builder /app/frontend/dist ./backend/app/static

WORKDIR /app/backend

# Railway injects $PORT dynamically
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

