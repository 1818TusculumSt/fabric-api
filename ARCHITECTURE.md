# Fabric MCP Server Architecture

## Overview

This is a **pure prompt delivery system**. The MCP server acts as a library that fetches and serves Fabric patterns (expert-crafted prompts) to Claude Desktop. All AI processing happens natively in Claude.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                     │
│  "Use extract_wisdom on this article: [paste article]"          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLAUDE DESKTOP                                │
│  • Receives user request                                        │
│  • Identifies MCP tool call needed                              │
│  • Calls Fabric MCP server                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FABRIC MCP SERVER (This Project)                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Tool: apply_fabric_pattern                               │  │
│  │  Input: pattern="extract_wisdom", input_text="[article]"  │  │
│  └────────────────────┬──────────────────────────────────────┘  │
│                       │                                          │
│                       ▼                                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Pattern Loader                                           │  │
│  │  1. Check local cache (~/.cache/fabric-mcp/)             │  │
│  │  2. If not cached, fetch from GitHub                     │  │
│  │  3. Cache for future use                                 │  │
│  └────────────────────┬──────────────────────────────────────┘  │
│                       │                                          │
│                       ▼                                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Pattern (Prompt) from Fabric Repository                 │  │
│  │  https://github.com/danielmiessler/fabric                │  │
│  │                                                           │  │
│  │  # IDENTITY and PURPOSE                                  │  │
│  │  You extract surprising, insightful information...       │  │
│  │                                                           │  │
│  │  # STEPS                                                 │  │
│  │  - Extract summary in 25 words                           │  │
│  │  - Extract 20-50 surprising ideas                        │  │
│  │  ...                                                      │  │
│  │                                                           │  │
│  │  # OUTPUT INSTRUCTIONS                                    │  │
│  │  - Only output Markdown                                  │  │
│  │  - Write IDEAS as exactly 16 words                       │  │
│  │  ...                                                      │  │
│  │                                                           │  │
│  │  INPUT:                                                   │  │
│  │  [article text here]                                     │  │
│  └────────────────────┬──────────────────────────────────────┘  │
│                       │                                          │
└───────────────────────┼──────────────────────────────────────────┘
                        │ Returns complete prompt
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLAUDE'S LLM                                  │
│  • Receives pattern prompt + user content                       │
│  • Processes locally (no external API)                          │
│  • Executes pattern instructions                                │
│  • Generates structured output                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         RESULT                                   │
│  # SUMMARY                                                       │
│  Article discusses AI safety concerns...                         │
│                                                                  │
│  # IDEAS                                                         │
│  - AI alignment requires human values to be precisely defined    │
│  - Current language models exhibit emergent reasoning abilities  │
│  ...                                                             │
│                                                                  │
│  # INSIGHTS                                                      │
│  - Scaling laws suggest capability improvements are predictable  │
│  ...                                                             │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Initial Setup (One-Time)

```
User configures Claude Desktop
         ↓
claude_desktop_config.json updated
         ↓
MCP Server registered
         ↓
Claude Desktop restarts
         ↓
MCP Server initialized
         ↓
Pattern list fetched from GitHub (227 patterns)
         ↓
Pattern list cached locally
```

### 2. Pattern Application (Every Use)

```
User requests pattern
         ↓
Claude Desktop identifies tool call
         ↓
MCP Server receives: {pattern: "extract_wisdom", input: "..."}
         ↓
Check cache for pattern
         ↓
If not cached: Fetch from GitHub → Cache locally
         ↓
Combine pattern prompt + user input
         ↓
Return complete prompt to Claude
         ↓
Claude processes with native LLM
         ↓
Result returned to user
```

## Components

### MCP Server (Python)

**File:** `fabric_mcp/server.py`

**Responsibilities:**
- Implement MCP protocol
- Fetch pattern list from GitHub
- Cache patterns locally
- Serve patterns to Claude
- Combine patterns with user input

**No AI Processing Here!** Just prompt delivery.

### GitHub Repository (Fabric)

**Source:** https://github.com/danielmiessler/fabric

**Structure:**
```
fabric/
├── data/
│   └── patterns/
│       ├── extract_wisdom/
│       │   └── system.md         ← Pattern prompt
│       ├── summarize/
│       │   └── system.md         ← Pattern prompt
│       └── [227+ other patterns]/
│           └── system.md
```

**Our server fetches:**
- Pattern list from `/data/patterns/` directory
- Individual patterns from `/data/patterns/{name}/system.md`

### Local Cache

**Location:** `~/.cache/fabric-mcp/`

**Contents:**
```
~/.cache/fabric-mcp/
├── patterns_list.json           ← List of all patterns
├── extract_wisdom.md            ← Cached pattern
├── summarize.md                 ← Cached pattern
└── [other cached patterns].md
```

**Benefits:**
- Offline access after first fetch
- Fast pattern loading
- Reduced GitHub API calls

### Claude Desktop

**Role:** MCP Client

**What it does:**
1. Interprets user's natural language request
2. Identifies which MCP tool to call
3. Calls MCP server with parameters
4. Receives prompt from MCP server
5. Processes with native LLM
6. Returns result to user

**What it doesn't do:**
- No external API calls (everything local)
- No vendor-specific configuration
- No rate limiting

## Why This Architecture?

### Advantages

**✅ No API Keys**
- No OpenAI, Anthropic, or other API keys needed
- No account management
- No billing concerns

**✅ No Rate Limits**
- Process unlimited content
- No throttling
- No usage quotas

**✅ Privacy**
- Everything processed locally in Claude
- No data sent to external services
- Patterns cached on your machine

**✅ Vendor Agnostic**
- Works with any LLM that supports MCP
- Not tied to specific AI provider
- Future-proof architecture

**✅ Offline Capable**
- After first fetch, patterns cached
- No internet needed for cached patterns
- Fast response times

**✅ Open Source**
- Patterns are open source (Fabric)
- Server is open source (this project)
- Fully auditable and modifiable

### Comparison to Traditional Approaches

#### Traditional AI Tool
```
User → Web App → API Key → OpenAI/Anthropic/etc → Result
        ↑                    ↑
     Rate Limits         External Processing
     Subscription        Privacy Concerns
```

#### Fabric MCP (This Project)
```
User → Claude Desktop → MCP Server → Prompt Library
                ↓
          Claude's Local LLM
                ↓
            Result
```

**No external dependencies!**

## MCP Protocol Details

### Tools Exposed

1. **apply_fabric_pattern**
   ```json
   {
     "name": "apply_fabric_pattern",
     "parameters": {
       "pattern": "extract_wisdom",
       "input_text": "article content here..."
     }
   }
   ```
   Returns: Complete prompt (pattern + input)

2. **list_fabric_patterns**
   ```json
   {
     "name": "list_fabric_patterns",
     "parameters": {
       "filter": "extract"  // optional
     }
   }
   ```
   Returns: List of matching patterns with descriptions

3. **get_fabric_pattern**
   ```json
   {
     "name": "get_fabric_pattern",
     "parameters": {
       "pattern": "extract_wisdom"
     }
   }
   ```
   Returns: Full pattern prompt text

### Resources Exposed

Each pattern is also available as an MCP resource:

```
fabric://pattern/extract_wisdom
fabric://pattern/summarize
fabric://pattern/analyze_claims
...
```

These can be read directly by MCP-compatible clients.

## Technical Stack

### Server Side
- **Language:** Python 3.10+
- **Framework:** MCP SDK (`mcp>=1.0.0`)
- **HTTP Client:** `httpx>=0.27.0`
- **Protocol:** stdio-based MCP

### Client Side
- **Client:** Claude Desktop (or any MCP client)
- **Protocol:** Model Context Protocol
- **Processing:** Native LLM (no external APIs)

### Pattern Source
- **Repository:** GitHub (danielmiessler/fabric)
- **Format:** Markdown (system prompts)
- **License:** MIT

## Scalability

### Current Implementation
- **Patterns:** 227+ and growing
- **Cache:** Unlimited local storage
- **Speed:** Instant (cached), ~1-2s (first fetch)
- **Concurrent Users:** N/A (local only)

### Future Enhancements
- Auto-update patterns from GitHub
- Pattern versioning
- Custom pattern injection
- Pattern search/indexing
- Pattern favorites

## Security

### What's Secure
- **No external processing** - Everything local
- **No secrets needed** - No API keys to steal
- **Open source** - Fully auditable code
- **Read-only GitHub access** - Only fetches public data

### Considerations
- **Patterns are untrusted** - Fetched from public GitHub
- **Cache is local** - Stored unencrypted on disk
- **No input validation** - Patterns pass through as-is

**Mitigation:** Patterns come from the official Fabric repository, maintained by a trusted open-source community.

## Contributing

Want to enhance the architecture?

### Possible Improvements
- Pattern caching TTL/expiration
- Pattern update notifications
- Custom pattern directories
- Pattern validation/linting
- Usage statistics
- Pattern ratings/favorites

See the main [README.md](README.md) for contribution guidelines.

---

**Bottom Line:** This is a simple, elegant architecture that delivers expert prompts to Claude with zero external dependencies. No APIs, no configuration, just great prompts! 🎨✨
