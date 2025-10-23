# Fabric API Server

A Dockerized OpenAPI server that provides access to [Daniel Miessler's Fabric](https://github.com/danielmiessler/fabric) AI patterns through MCPO (MCP-to-OpenAPI proxy). Access 227+ expert-crafted prompts for tasks like extracting wisdom, summarizing content, analyzing arguments, creating visualizations, and much more!

Perfect for **Open WebUI**, API integrations, and any tool that supports OpenAPI/REST endpoints.

> **No API keys needed!** Fabric patterns are pure prompts - this server delivers them to your LLM, which processes everything natively. No external AI services, no vendor lock-in, no rate limits.

> **🔄 Auto-Updates!** The server automatically checks for new patterns daily. Always stay current with the latest Fabric patterns!

## 🚀 Quick Start

Run Fabric as an OpenAPI server for **Open WebUI** and other tools using Docker:

```bash
# Quick start with Docker
cp .env.example .env
# Edit .env and set your MCPO_API_KEY
docker-compose up -d

# Access at http://localhost:8000
# API docs at http://localhost:8000/docs
```

**[📖 See OPENWEBUI_SETUP.md for complete setup guide](OPENWEBUI_SETUP.md)**

## 📚 Documentation

- **[OPENWEBUI_SETUP.md](OPENWEBUI_SETUP.md)** - Complete Docker + Open WebUI setup guide
- **[PROMPTING_STRATEGIES.md](PROMPTING_STRATEGIES.md)** - How to use patterns effectively
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - How the system works

## What is Fabric?

Fabric is an open-source framework for augmenting humans using AI. It provides a modular system of expert-crafted prompts (called "patterns") for solving specific problems. Each pattern is a carefully designed system prompt optimized for tasks like:

- **extract_wisdom** - Extract insights, ideas, quotes, and recommendations
- **summarize** - Create concise summaries
- **analyze_claims** - Evaluate arguments and claims
- **create_markmap** - Generate mind map visualizations
- **explain_code** - Explain code in plain language
- **improve_writing** - Enhance written content
- And 227+ more patterns!

## Features

- **🐳 Docker Ready** - Single command deployment with Docker Compose
- **🔌 OpenAPI/REST** - Standard HTTP endpoints via MCPO proxy
- **🌐 Open WebUI Integration** - Works seamlessly with Open WebUI
- **📦 227+ Fabric Patterns** - All patterns from the official Fabric repository
- **🔄 Auto-Caching** - Patterns are cached locally for fast access
- **🎯 Pure Prompts** - No API keys, no external services required
- **🔍 Pattern Search** - List and filter available patterns
- **📖 Pattern Details** - View full prompts for any pattern

## Available API Endpoints

### 1. `apply_fabric_pattern`
Apply any Fabric pattern to input text.

**Parameters:**
- `pattern` - The name of the pattern to apply
- `input_text` - The text content to process

### 2. `list_fabric_patterns`
List all available patterns, optionally filtered by keyword.

**Parameters:**
- `filter` (optional) - Filter patterns by name

### 3. `get_fabric_pattern`
Get the full prompt/instructions for a specific pattern.

**Parameters:**
- `pattern` - The name of the pattern

### 4. `update_fabric_patterns`
Force an immediate update of the pattern list from GitHub.

## Popular Patterns

- **extract_wisdom** - Extract insights, ideas, quotes, habits, facts, and recommendations
- **summarize** - Create concise summaries
- **explain_code** - Explain code in plain language
- **improve_writing** - Enhance written content
- **create_markmap** - Generate markmap visualizations
- **analyze_claims** - Analyze and evaluate claims
- **create_visualization** - Create visual representations
- **rate_content** - Rate content quality
- **find_logical_fallacies** - Identify logical fallacies

And many more! Use the `list_fabric_patterns` endpoint to see all available patterns.

## Architecture

```
┌─────────────┐
│ Open WebUI  │
│  or Client  │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────┐
│    MCPO     │  (MCP-to-OpenAPI Proxy)
└──────┬──────┘
       │ MCP Protocol
       ▼
┌─────────────┐
│ Fabric MCP  │  (Fetches patterns from GitHub)
│   Server    │
└─────────────┘
```

## Configuration

Edit `.env` to customize:

- `MCPO_PORT`: Port for the MCPO server (default: 8000)
- `MCPO_API_KEY`: API key for authentication (required)
- `FABRIC_CACHE_TTL_HOURS`: How often to check for pattern updates (default: 24)
- `FABRIC_AUTO_UPDATE`: Automatically update patterns (default: true)

## Use Cases

### With Open WebUI
Integrate all Fabric patterns directly into your Open WebUI instance for enhanced AI conversations.

### As a Microservice
Use Fabric patterns in your application stack via standard REST API calls.

### Pattern Chaining
Combine multiple patterns for complex workflows:
```
1. extract_wisdom → Get insights
2. summarize → Condense insights
3. create_quiz → Test knowledge
```

## Credits & Attribution

- **Fabric Framework** by [Daniel Miessler](https://github.com/danielmiessler)
- All patterns from the [Fabric repository](https://github.com/danielmiessler/fabric)
- Built with [Model Context Protocol](https://modelcontextprotocol.io)
- Powered by [MCPO](https://github.com/open-webui/mcpo) (MCP-to-OpenAPI proxy)
- MCP server implementation inspired by the Fabric MCP community

## License

MIT License - See [LICENSE](LICENSE) file for details

The Fabric patterns themselves are from the Fabric project and maintain their original MIT license.

## Contributing

Contributions welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues with:
- **This API Server** - Open an issue in this repository
- **Fabric Patterns** - See the [Fabric repository](https://github.com/danielmiessler/fabric)
- **MCPO** - See the [MCPO repository](https://github.com/open-webui/mcpo)
- **Open WebUI** - See [Open WebUI docs](https://docs.openwebui.com)

---

**Ready to supercharge your AI workflows with Fabric patterns!** 🚀✨
