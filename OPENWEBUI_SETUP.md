# Fabric MCPO Server for Open WebUI

This guide explains how to run the Fabric MCP server as an OpenAPI-compatible service for Open WebUI using MCPO (MCP-to-OpenAPI proxy).

## What is MCPO?

MCPO is a proxy that converts MCP (Model Context Protocol) servers into standard OpenAPI/REST endpoints. This allows you to use Fabric patterns with any tool that supports OpenAPI, including Open WebUI.

## Quick Start with Docker

### 1. Clone and Configure

```bash
# Clone the repository
git clone <your-repo-url>
cd fabric-api

# Create environment file
cp .env.example .env

# Edit .env and set a secure API key
# Change MCPO_API_KEY to something secure!
```

### 2. Start the Server

```bash
# Build and start the container
docker-compose up -d

# Check logs
docker-compose logs -f fabric-mcpo
```

The server will be available at `http://localhost:8000`

### 3. Test the API

Visit `http://localhost:8000/docs` to see the interactive OpenAPI documentation and test the endpoints.

## Integrating with Open WebUI

### Option 1: Docker Compose (Recommended)

Edit `docker-compose.yml` and uncomment the `open-webui` service section, then:

```bash
docker-compose up -d
```

Open WebUI will be available at `http://localhost:3000` and automatically configured to use the Fabric MCPO server.

### Option 2: Existing Open WebUI Instance

If you already have Open WebUI running:

1. Go to **Settings** > **Connections** (or Admin Panel)
2. Add a new OpenAPI connection:
   - **Name**: Fabric Patterns
   - **Base URL**: `http://fabric-mcpo:8000` (if using Docker network) or `http://localhost:8000`
   - **API Key**: Your `MCPO_API_KEY` from `.env`

### Option 3: Open WebUI with Different Network

If Open WebUI is on a different Docker network or host:

```bash
# Get your host IP
# Linux/Mac: ip addr show or ifconfig
# Windows: ipconfig

# Use your host IP in Open WebUI settings
# Base URL: http://<your-ip>:8000
```

## Available API Endpoints

Once MCPO is running, you'll have access to these endpoints:

### List All Patterns
```bash
curl -H "Authorization: Bearer your-api-key" \
  http://localhost:8000/list_fabric_patterns
```

### Apply a Pattern
```bash
curl -X POST -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"pattern": "extract_wisdom", "input_text": "Your content here..."}' \
  http://localhost:8000/apply_fabric_pattern
```

### Get Pattern Details
```bash
curl -H "Authorization: Bearer your-api-key" \
  http://localhost:8000/get_fabric_pattern?pattern=summarize
```

### Update Patterns
```bash
curl -X POST -H "Authorization: Bearer your-api-key" \
  http://localhost:8000/update_fabric_patterns
```

## Configuration

### Environment Variables

Edit `.env` to customize:

- `MCPO_PORT`: Port for the MCPO server (default: 8000)
- `MCPO_API_KEY`: API key for authentication (required)
- `FABRIC_CACHE_TTL_HOURS`: How often to check for pattern updates (default: 24)
- `FABRIC_AUTO_UPDATE`: Automatically update patterns (default: true)

### Cache Location

Pattern cache is stored in a Docker volume named `fabric-cache`. To clear the cache:

```bash
docker-compose down
docker volume rm fabric-api_fabric-cache
docker-compose up -d
```

## Using Patterns in Open WebUI

Once configured, you can use Fabric patterns in Open WebUI conversations:

### Example Prompts

**Extract Wisdom:**
```
Use the Fabric extract_wisdom tool to analyze this article:
[paste article text]
```

**Summarize Content:**
```
Apply the Fabric summarize pattern to this document:
[paste document]
```

**List Available Patterns:**
```
Show me all available Fabric patterns related to "analysis"
```

## Troubleshooting

### Server won't start

Check logs:
```bash
docker-compose logs fabric-mcpo
```

Common issues:
- Port 8000 already in use: Change `MCPO_PORT` in `.env`
- Missing API key: Set `MCPO_API_KEY` in `.env`

### Open WebUI can't connect

1. Verify the server is running:
   ```bash
   curl http://localhost:8000/docs
   ```

2. Check Docker network:
   ```bash
   docker network inspect fabric-api_fabric-network
   ```

3. Test with correct API key:
   ```bash
   curl -H "Authorization: Bearer your-api-key" http://localhost:8000/health
   ```

### Patterns not updating

Force an update:
```bash
curl -X POST -H "Authorization: Bearer your-api-key" \
  http://localhost:8000/update_fabric_patterns
```

Or restart the container:
```bash
docker-compose restart fabric-mcpo
```

## Advanced Usage

### Custom Port

```bash
# Edit .env
MCPO_PORT=9000

# Restart
docker-compose up -d
```

### Disable Auto-Updates

```bash
# Edit .env
FABRIC_AUTO_UPDATE=false

# Restart
docker-compose up -d
```

### Running Behind a Reverse Proxy

If running behind nginx or traefik, you may need to set the `--root-path` flag. Edit the `Dockerfile` CMD:

```dockerfile
CMD mcpo --port ${MCPO_PORT} --root-path "/api/fabric" --api-key "${MCPO_API_KEY}" -- python -m fabric_mcp.server
```

### Production Deployment

For production:

1. Use a strong API key
2. Consider HTTPS termination with nginx/traefik
3. Set up monitoring and logging
4. Use Docker secrets instead of environment variables

Example nginx config:
```nginx
location /fabric/ {
    proxy_pass http://localhost:8000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## Architecture

```
┌─────────────┐
│ Open WebUI  │
└──────┬──────┘
       │ HTTP/OpenAPI
       ▼
┌─────────────┐
│    MCPO     │  (Converts OpenAPI ↔ MCP)
└──────┬──────┘
       │ MCP Protocol
       ▼
┌─────────────┐
│ Fabric MCP  │  (Fetches patterns from GitHub)
│   Server    │
└─────────────┘
```

## Resources

- [MCPO Documentation](https://github.com/open-webui/mcpo)
- [Open WebUI Documentation](https://docs.openwebui.com)
- [Fabric Patterns Repository](https://github.com/danielmiessler/fabric)
- [MCP Protocol Specification](https://modelcontextprotocol.io)

## Support

For issues:
- **MCPO Server**: Check [MCPO GitHub](https://github.com/open-webui/mcpo)
- **Fabric Patterns**: See [Fabric Repository](https://github.com/danielmiessler/fabric)
- **This Integration**: Open an issue in this repository
