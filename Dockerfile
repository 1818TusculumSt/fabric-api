# Dockerfile for Fabric MCP Server with MCPO
# This allows the Fabric MCP server to be exposed as an OpenAPI endpoint for Open WebUI

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY fabric_mcp/ ./fabric_mcp/
COPY README.md ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Install MCPO
RUN pip install --no-cache-dir mcpo

# Create cache directory
RUN mkdir -p /root/.cache/fabric-mcp

# Expose port for MCPO
EXPOSE 8000

# Environment variables (can be overridden)
ENV FABRIC_CACHE_TTL_HOURS=24
ENV FABRIC_AUTO_UPDATE=true
ENV MCPO_PORT=8000
ENV MCPO_API_KEY=fabric-secret-key

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${MCPO_PORT}/health || exit 1

# Start MCPO with the Fabric MCP server
CMD mcpo --port ${MCPO_PORT} --api-key "${MCPO_API_KEY}" -- python -m fabric_mcp.server
