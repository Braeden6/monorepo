FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml ./
COPY .python-version ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY src ./src

# Expose port
EXPOSE 8001

# Run the application
CMD ["uv", "run", "uvicorn", "recipe_api.main:app", "--host", "0.0.0.0", "--port", "8001"]
