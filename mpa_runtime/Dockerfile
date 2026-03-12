# Use a slim Python image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy uv binary from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies using uv
# --system is used because we are in a container and don't need a venv
RUN uv pip install --system .

# Copy the application code
COPY main.py .
COPY mpa/ ./mpa/

# Cloud Run sets the PORT environment variable.
# main.py already uses os.getenv("PORT", 8000)
ENV PORT=8080

# Command to run the application
CMD ["python", "main.py"]
