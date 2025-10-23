# Automatic Pattern Updates

The Fabric MCP server automatically keeps your pattern library up to date with the latest patterns from the official Fabric repository!

## How It Works

### On Startup

Every time Claude Desktop restarts (which initializes the MCP server), the server:

1. **Checks cache age** - Looks at when patterns were last fetched
2. **Compares to TTL** - Default: 24 hours
3. **Updates if needed** - Fetches latest patterns from GitHub if cache is old
4. **Reports changes** - Logs new or removed patterns

### Cache Management

Patterns are cached in `~/.cache/fabric-mcp/` with metadata:

```
~/.cache/fabric-mcp/
├── patterns_list.json          ← Pattern names
├── patterns_list_meta.json     ← Timestamp, count, version
├── extract_wisdom.md           ← Cached pattern content
└── ...
```

### Update Logic

```
Server starts
    ↓
Check cache age
    ↓
If older than 24h (configurable)
    ↓
Fetch from GitHub
    ↓
Compare old vs new
    ↓
Report changes:
  - ✨ New patterns added
  - ⚠️  Patterns removed
    ↓
Update cache
```

## Configuration

### Change Update Interval

Set the cache TTL (time to live) in hours:

**Windows - PowerShell:**
```powershell
$env:FABRIC_CACHE_TTL_HOURS="12"  # Check every 12 hours
```

**Windows - claude_desktop_config.json:**
```json
{
  "mcpServers": {
    "fabric": {
      "command": "python",
      "args": ["-m", "fabric_mcp.server"],
      "env": {
        "FABRIC_CACHE_TTL_HOURS": "12"
      }
    }
  }
}
```

**macOS/Linux:**
```bash
export FABRIC_CACHE_TTL_HOURS=12
```

### Disable Auto-Update

If you want to control updates manually:

```json
{
  "mcpServers": {
    "fabric": {
      "command": "python",
      "args": ["-m", "fabric_mcp.server"],
      "env": {
        "FABRIC_AUTO_UPDATE": "false"
      }
    }
  }
}
```

When disabled, the server uses cached patterns indefinitely.

### Recommended TTL Values

| Use Case | TTL (hours) | Why |
|----------|-------------|-----|
| **Active Development** | 1-6 | Get latest patterns quickly |
| **Normal Use** | 24 (default) | Balance freshness & API calls |
| **Stable Production** | 168 (7 days) | Minimize GitHub API usage |
| **Offline/Controlled** | Disabled | Manual updates only |

## Manual Update

### Using the MCP Tool

You can force an update anytime through Claude Desktop:

```
Update my Fabric patterns
```

or more explicitly:

```
Use the update_fabric_patterns tool to check for new patterns
```

### Response Example

```markdown
# Pattern Update Complete

- Previous patterns: 225
- Current patterns: 227
- **2 new patterns added!** 🎉

Pattern list has been refreshed from GitHub.
```

### From Command Line

Delete the cache metadata to force an update on next startup:

**Windows:**
```powershell
Remove-Item "$env:USERPROFILE\.cache\fabric-mcp\patterns_list_meta.json"
```

**macOS/Linux:**
```bash
rm ~/.cache/fabric-mcp/patterns_list_meta.json
```

## What Gets Updated

### Pattern List

The list of available patterns (227+ and growing):
- ✅ New patterns are added
- ✅ Removed patterns are deleted
- ✅ Changes are logged

### Pattern Content

Individual pattern prompts are also cached with updates:

- **First use**: Pattern fetched from GitHub, cached
- **Subsequent uses**: Pattern loaded from cache
- **Cache persists**: Patterns cached indefinitely for offline use
- **Manual refresh**: Delete pattern file to re-fetch

To refresh a specific pattern:

**Windows:**
```powershell
Remove-Item "$env:USERPROFILE\.cache\fabric-mcp\extract_wisdom.md"
```

**macOS/Linux:**
```bash
rm ~/.cache/fabric-mcp/extract_wisdom.md
```

Next time you use it, it'll fetch the latest version.

## Update Notifications

The server logs pattern updates:

```
INFO:fabric-mcp-server:Fetching latest patterns from GitHub...
INFO:fabric-mcp-server:✨ New patterns available: analyze_incident, create_git_diff_commit
INFO:fabric-mcp-server:Updated from 225 to 227 patterns
```

Check Claude Desktop logs to see update history:

**Windows:** `%APPDATA%\Claude\logs`
**macOS:** `~/Library/Logs/Claude`
**Linux:** `~/.config/Claude/logs`

## GitHub API Rate Limits

GitHub allows **60 requests/hour** without authentication for public repositories.

### Our Usage:

- **Pattern list update**: 1 API call per update check
- **Pattern content fetch**: 1 API call per new pattern (cached after)

### Typical Usage:

- Restart Claude Desktop 10 times/day = 10 API calls
- Use 20 new patterns/day = 20 API calls
- **Total: 30 API calls/day** (well within limit)

### If You Hit the Limit:

Very unlikely, but if it happens:

1. **Wait 1 hour** - Limits reset hourly
2. **Use cached patterns** - Server falls back automatically
3. **Add GitHub token** (optional) - Increases limit to 5,000/hour

#### Adding GitHub Token (Optional):

```json
{
  "mcpServers": {
    "fabric": {
      "command": "python",
      "args": ["-m", "fabric_mcp.server"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

Create a token at: https://github.com/settings/tokens (no permissions needed for public repos)

## Offline Support

### First Time Setup

Requires internet to download patterns initially.

### After Initial Download

Works completely offline!

- ✅ All 227+ patterns cached locally
- ✅ Pattern content cached indefinitely
- ✅ No internet needed for daily use
- ✅ Updates only require internet

### Travel/Offline Workflow

1. **Before going offline**: Use `update_fabric_patterns` tool
2. **While offline**: Use all cached patterns normally
3. **After reconnecting**: Server auto-updates on next restart

## Update Scenarios

### Scenario 1: New Pattern Added to Fabric

```
Day 1: Fabric repo adds "analyze_quantum_code" pattern
    ↓
Day 2: You restart Claude Desktop (cache > 24h old)
    ↓
Server fetches updates
    ↓
Logs: "✨ New patterns available: analyze_quantum_code"
    ↓
Pattern immediately available for use!
```

### Scenario 2: Pattern Content Updated

```
Fabric team improves "extract_wisdom" prompt
    ↓
You delete: ~/.cache/fabric-mcp/extract_wisdom.md
    ↓
Next time you use extract_wisdom:
    ↓
Server fetches latest version from GitHub
    ↓
New improved pattern is cached
```

### Scenario 3: Pattern Removed from Fabric

```
Fabric repo removes deprecated "old_pattern"
    ↓
Server updates pattern list
    ↓
Logs: "⚠️ Patterns removed: old_pattern"
    ↓
Pattern no longer appears in list_fabric_patterns
```

## Troubleshooting

### Patterns not updating

**Check auto-update is enabled:**
```json
"env": {
  "FABRIC_AUTO_UPDATE": "true"  ← Make sure this is true
}
```

**Check cache age:**
- Cache only updates if older than TTL
- Default: 24 hours
- Lower TTL for more frequent updates

**Force update:**
```
Use the update_fabric_patterns tool
```

### Update errors

**Network issues:**
```
ERROR: Error fetching patterns from GitHub: ...
INFO: Using cached patterns (227 patterns)
```

**Solution**: Server automatically falls back to cache. Try again when internet is available.

**GitHub rate limit:**
```
ERROR: ... rate limit exceeded ...
INFO: Using cached patterns
```

**Solution**: Wait 1 hour, or add GitHub token (see above)

### Cache corruption

If cache gets corrupted, delete it:

**Windows:**
```powershell
Remove-Item -Recurse "$env:USERPROFILE\.cache\fabric-mcp\"
```

**macOS/Linux:**
```bash
rm -rf ~/.cache/fabric-mcp/
```

Server will rebuild cache on next use.

## Best Practices

### For Most Users

✅ **Use defaults** (24h TTL, auto-update enabled)
- Patterns stay fresh
- Minimal GitHub API usage
- Works offline after initial download

### For Developers

✅ **Set shorter TTL** (6-12h) when actively following Fabric development
```json
"FABRIC_CACHE_TTL_HOURS": "6"
```

### For Offline Users

✅ **Pre-download patterns before going offline**
```
Use update_fabric_patterns tool
```

✅ **Disable auto-update to prevent errors**
```json
"FABRIC_AUTO_UPDATE": "false"
```

### For CI/CD or Automation

✅ **Disable auto-update** for reproducibility
```json
"FABRIC_AUTO_UPDATE": "false"
```

✅ **Pre-populate cache** in build step
```bash
python -m fabric_mcp.server --update-cache
```

## Future Enhancements

Possible improvements:

- [ ] Pattern versioning (track pattern changes over time)
- [ ] Selective pattern updates (update only specific patterns)
- [ ] Pattern diffing (see what changed in a pattern)
- [ ] Update notifications in Claude Desktop UI
- [ ] Background update (update while server is running)
- [ ] Pattern favorites (pin specific pattern versions)

Want to contribute? See [README.md](README.md) for contribution guidelines!

---

**Bottom Line**: The Fabric MCP server keeps your patterns fresh automatically, with zero configuration needed. Just restart Claude Desktop periodically, and you'll always have the latest patterns! 🎨✨
