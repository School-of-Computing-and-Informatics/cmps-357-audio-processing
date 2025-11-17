# ============================
# Stage 1: Builder
# ============================
FROM python:3.12-slim AS builder

# Install system build dependencies and FFmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        gcc \
        g++ \
        make \
        libsndfile1-dev \
        libffi-dev \
        libssl-dev \
        git && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy dependency lists first (for caching)
COPY requirements.txt .

# Install Python dependencies into a clean directory
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# ============================
# Stage 2: Final Runtime Image
# ============================
FROM python:3.12-slim AS runtime

# Install FFmpeg only (no build tools)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set up app directory
WORKDIR /

# Copy installed Python packages from builder stage
COPY --from=builder /install /usr/local

# Copy project source
COPY . .

# Expose Flask port (adjust if needed)
EXPOSE 5000

# Environment settings for Flask
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Create a directory for uploaded/processed audio
RUN mkdir -p /app/data

# Default command (adjust your entrypoint script if needed)
CMD ["python", "run.py"]
