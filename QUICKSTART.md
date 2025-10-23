# Fabric MCP Server - Quick Start Guide

Get up and running with Fabric patterns in Claude Desktop in 5 minutes!

## Step 1: Install

```bash
cd "C:\Users\jonat\OneDrive\Coding Projects\fabric-mcp"
pip install -e .
```

## Step 2: Configure Claude Desktop

1. Open your Claude Desktop config file:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. Add this configuration (or merge with existing config):

```json
{
  "mcpServers": {
    "fabric": {
      "command": "python",
      "args": [
        "-m",
        "fabric_mcp.server"
      ]
    }
  }
}
```

## Step 3: Restart Claude Desktop

Close Claude Desktop completely and reopen it.

## Step 4: Try It Out!

Open Claude Desktop and try these commands:

### List all patterns
```
List all available Fabric patterns
```

### Use extract_wisdom pattern
```
Use the extract_wisdom Fabric pattern on this text:

[Paste any article, transcript, or content here]
```

### Use summarize pattern
```
Apply the summarize pattern to this content:

[Paste content here]
```

### See what a pattern does
```
Show me the full prompt for the analyze_claims pattern
```

## Popular Patterns to Try

- **extract_wisdom** - Extract insights, quotes, ideas, and recommendations
- **summarize** - Create concise summaries
- **improve_writing** - Enhance your writing
- **explain_code** - Get plain language code explanations
- **create_quiz** - Generate quiz questions from content
- **analyze_claims** - Evaluate arguments and claims
- **find_logical_fallacies** - Identify logical errors

## Troubleshooting

### Server not showing up?

1. Check that your config JSON is valid (use a JSON validator)
2. Make sure Python is in your PATH
3. Restart Claude Desktop completely
4. Check Claude logs:
   - Windows: `%APPDATA%\Claude\logs`
   - macOS: `~/Library/Logs/Claude`

### Patterns not loading?

- First time loading patterns requires internet connection
- Patterns are cached in `~/.cache/fabric-mcp/` for offline use
- Check the Claude Desktop logs for errors

## Next Steps

- Browse all 100+ patterns: `list_fabric_patterns`
- Read the full [README.md](README.md) for detailed documentation
- Check out the [Fabric repository](https://github.com/danielmiessler/fabric) for pattern updates

---

Enjoy! 🎨✨
