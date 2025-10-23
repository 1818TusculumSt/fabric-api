# Fabric MCP Server - Project Summary

## What This Does

This MCP server gives Claude Desktop access to **all 227+ Fabric AI patterns** from Daniel Miessler's [Fabric framework](https://github.com/danielmiessler/fabric).

Fabric patterns are expert-crafted prompts for common AI tasks:
- Extract wisdom from content
- Summarize articles and videos
- Analyze claims and arguments
- Create visualizations
- Explain code
- Improve writing
- And 200+ more patterns!

## Project Structure

```
fabric-mcp/
├── fabric_mcp/
│   ├── __init__.py          # Package initialization
│   └── server.py            # Main MCP server implementation
├── pyproject.toml           # Python project configuration
├── requirements.txt         # Python dependencies
├── test_server.py           # Test script
├── README.md                # Full documentation
├── QUICKSTART.md            # Quick setup guide
├── LICENSE                  # MIT license
└── claude_desktop_config.example.json  # Example config
```

## How It Works

1. **Pattern Discovery** - Server fetches the list of all available patterns from the Fabric GitHub repository
2. **Local Caching** - Patterns are cached in `~/.cache/fabric-mcp/` for fast offline access
3. **MCP Tools** - Provides 3 MCP tools:
   - `apply_fabric_pattern` - Apply any pattern to your text
   - `list_fabric_patterns` - Browse available patterns
   - `get_fabric_pattern` - View a pattern's prompt
4. **MCP Resources** - Each pattern is available as a resource at `fabric://pattern/{name}`

## Features

- ✅ **227+ Fabric Patterns** - Full access to all official patterns
- ✅ **Automatic Updates** - Fetches latest patterns from GitHub
- ✅ **Local Caching** - Works offline after first use
- ✅ **Smart Search** - Filter patterns by keyword
- ✅ **Easy to Use** - Natural language interface through Claude Desktop

## Installation

```bash
# Install the server
cd "C:\Users\jonat\OneDrive\Coding Projects\fabric-mcp"
pip install -e .

# Test it works
python test_server.py
```

## Configuration

Add to Claude Desktop config (`%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "fabric": {
      "command": "python",
      "args": ["-m", "fabric_mcp.server"]
    }
  }
}
```

Restart Claude Desktop and you're ready!

## Usage Examples

Once configured, you can use Fabric patterns in Claude Desktop:

```
List all Fabric patterns
```

```
Use the extract_wisdom pattern on this article: [paste article]
```

```
Apply the summarize pattern to this video transcript: [paste transcript]
```

```
Show me the improve_writing pattern
```

## Technical Details

- **Language**: Python 3.10+
- **Dependencies**:
  - `mcp>=1.0.0` - Model Context Protocol SDK
  - `httpx>=0.27.0` - HTTP client for GitHub API
- **Pattern Source**: https://github.com/danielmiessler/fabric/tree/main/data/patterns
- **Cache Location**: `~/.cache/fabric-mcp/`
- **Protocol**: MCP (Model Context Protocol)

## Testing

The test suite verifies:
1. Pattern list loading from GitHub
2. Individual pattern fetching
3. Pattern caching
4. Description generation

Run tests with:
```bash
python test_server.py
```

Expected output:
```
[SUCCESS] All tests passed! Server is working correctly.
```

## Credits

- **Fabric Framework** by Daniel Miessler - https://github.com/danielmiessler/fabric
- **MCP Protocol** by Anthropic - https://modelcontextprotocol.io
- All patterns are from the Fabric project (MIT License)

## Next Steps

1. **Install** - Follow QUICKSTART.md
2. **Try It** - Use patterns in Claude Desktop
3. **Explore** - Browse all 227+ patterns
4. **Share** - Help others discover Fabric patterns!

---

**Happy prompting!** 🎨✨
