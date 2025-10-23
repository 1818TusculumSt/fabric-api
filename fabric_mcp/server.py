#!/usr/bin/env python3
"""
Fabric MCP Server

Provides access to Daniel Miessler's Fabric AI patterns through MCP.
Each pattern is exposed as an MCP tool that can apply the pattern to input text.
"""

import asyncio
import json
import logging
import os
import time
from typing import Any
from pathlib import Path

import httpx
from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
import mcp.server.stdio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fabric-mcp-server")

# Constants
FABRIC_REPO = "danielmiessler/fabric"
FABRIC_BRANCH = "main"
PATTERNS_PATH = "data/patterns"
GITHUB_API_BASE = "https://api.github.com"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com"

# Cache settings (configurable via environment variables)
CACHE_TTL_HOURS = int(os.getenv("FABRIC_CACHE_TTL_HOURS", "24"))  # Default: 24 hours
AUTO_UPDATE = os.getenv("FABRIC_AUTO_UPDATE", "true").lower() == "true"  # Default: enabled

# Cache for patterns
patterns_cache = {}
patterns_list = []


class FabricMCPServer:
    """MCP Server for Fabric patterns."""

    def __init__(self):
        self.server = Server("fabric-mcp-server")
        self.http_client = httpx.AsyncClient(timeout=30.0)
        self.cache_dir = Path.home() / ".cache" / "fabric-mcp"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.patterns_list = []
        self.patterns_cache = {}

        # Setup handlers
        self.setup_handlers()

    def setup_handlers(self):
        """Setup MCP protocol handlers."""

        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List available Fabric patterns as resources."""
            await self._ensure_patterns_loaded()

            resources = []
            for pattern_name in self.patterns_list:
                resources.append(
                    Resource(
                        uri=f"fabric://pattern/{pattern_name}",
                        name=f"Fabric Pattern: {pattern_name}",
                        mimeType="text/markdown",
                        description=f"The '{pattern_name}' Fabric AI pattern prompt"
                    )
                )
            return resources

        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read a specific Fabric pattern."""
            if not uri.startswith("fabric://pattern/"):
                raise ValueError(f"Unknown resource URI: {uri}")

            pattern_name = uri.replace("fabric://pattern/", "")
            pattern_content = await self._get_pattern(pattern_name)

            return pattern_content

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available Fabric pattern tools."""
            await self._ensure_patterns_loaded()

            tools = []

            # Add a general "apply_pattern" tool
            tools.append(
                Tool(
                    name="apply_fabric_pattern",
                    description=(
                        "Apply any Fabric AI pattern to input text. "
                        "Fabric patterns are expert-crafted prompts for tasks like extracting wisdom, "
                        "summarizing content, analyzing arguments, creating visualizations, and much more."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pattern": {
                                "type": "string",
                                "description": f"The pattern to apply. Available patterns: {', '.join(sorted(self.patterns_list[:20]))}... (and many more)",
                                "enum": sorted(self.patterns_list)
                            },
                            "input_text": {
                                "type": "string",
                                "description": "The text content to process with the pattern"
                            }
                        },
                        "required": ["pattern", "input_text"]
                    }
                )
            )

            # Add a tool to list all patterns
            tools.append(
                Tool(
                    name="list_fabric_patterns",
                    description="List all available Fabric patterns with their descriptions",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filter": {
                                "type": "string",
                                "description": "Optional filter to search patterns by name (e.g., 'extract', 'analyze', 'create')"
                            }
                        }
                    }
                )
            )

            # Add a tool to get pattern details
            tools.append(
                Tool(
                    name="get_fabric_pattern",
                    description="Get the full prompt/instructions for a specific Fabric pattern",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pattern": {
                                "type": "string",
                                "description": "The name of the pattern to retrieve",
                                "enum": sorted(self.patterns_list)
                            }
                        },
                        "required": ["pattern"]
                    }
                )
            )

            # Add a tool to update patterns
            tools.append(
                Tool(
                    name="update_fabric_patterns",
                    description="Force an update of the pattern list from GitHub. Use this to get the latest patterns immediately.",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            )

            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool calls."""

            if name == "apply_fabric_pattern":
                pattern = arguments["pattern"]
                input_text = arguments["input_text"]

                # Get the pattern content
                pattern_content = await self._get_pattern(pattern)

                # Check if this is a t_ pattern that mentions TELOS
                telos_note = ""
                if pattern.startswith("t_") and "TELOS" in pattern_content.upper():
                    telos_note = (
                        "\n\n# IMPORTANT NOTE ABOUT TELOS FILES:\n\n"
                        "This pattern references a 'TELOS File' in its instructions. This is OPTIONAL context about a person/entity. "
                        "If no TELOS file is provided in the input, interpret the input as the primary content to analyze and adapt "
                        "the pattern steps accordingly. You can process ANY input through this pattern - the TELOS file is not required. "
                        "Work with whatever input is provided.\n"
                    )

                # Create an instruction for Claude to process the input with the pattern
                instruction = (
                    f"You are now acting as the Fabric AI pattern '{pattern}'. "
                    f"Apply the following pattern instructions to the provided input and return ONLY the processed output.{telos_note}\n"
                    f"# PATTERN INSTRUCTIONS:\n\n{pattern_content}\n\n"
                    f"# INPUT TO PROCESS:\n\n{input_text}\n\n"
                    f"# YOUR TASK:\n\n"
                    f"Follow the pattern instructions above precisely and process the input. "
                    f"If the pattern mentions optional files (like TELOS files) that aren't provided, skip those steps and work with the input provided. "
                    f"Return only the final output as specified by the pattern - do not include explanations, "
                    f"meta-commentary, or questions about missing files. Act as if you are the pattern itself."
                )

                return [
                    TextContent(
                        type="text",
                        text=instruction
                    )
                ]

            elif name == "list_fabric_patterns":
                filter_text = arguments.get("filter", "").lower()

                # Filter patterns if requested
                if filter_text:
                    filtered = [p for p in self.patterns_list if filter_text in p.lower()]
                else:
                    filtered = self.patterns_list

                # Create a formatted list
                pattern_list_text = f"# Fabric Patterns ({len(filtered)} patterns)\n\n"
                pattern_list_text += "Here are the available Fabric AI patterns:\n\n"

                for pattern in sorted(filtered):
                    pattern_list_text += f"- **{pattern}**: {self._get_pattern_description(pattern)}\n"

                return [
                    TextContent(
                        type="text",
                        text=pattern_list_text
                    )
                ]

            elif name == "get_fabric_pattern":
                pattern = arguments["pattern"]
                pattern_content = await self._get_pattern(pattern)

                return [
                    TextContent(
                        type="text",
                        text=f"# Fabric Pattern: {pattern}\n\n{pattern_content}"
                    )
                ]

            elif name == "update_fabric_patterns":
                # Force update by clearing cache timestamp
                cache_meta_file = self.cache_dir / "patterns_list_meta.json"
                if cache_meta_file.exists():
                    cache_meta_file.unlink()

                old_count = len(self.patterns_list)
                await self._load_patterns_list()
                new_count = len(self.patterns_list)

                status_text = f"# Pattern Update Complete\n\n"
                status_text += f"- Previous patterns: {old_count}\n"
                status_text += f"- Current patterns: {new_count}\n"

                if new_count > old_count:
                    status_text += f"- **{new_count - old_count} new patterns added!** 🎉\n"
                elif new_count < old_count:
                    status_text += f"- {old_count - new_count} patterns removed\n"
                else:
                    status_text += f"- No changes detected\n"

                status_text += f"\nPattern list has been refreshed from GitHub."

                return [
                    TextContent(
                        type="text",
                        text=status_text
                    )
                ]

            else:
                raise ValueError(f"Unknown tool: {name}")

    def _get_pattern_description(self, pattern_name: str) -> str:
        """Generate a description for a pattern based on its name."""
        # Simple heuristic descriptions based on common pattern names
        descriptions = {
            "extract_wisdom": "Extract insights, ideas, quotes, and recommendations from content",
            "summarize": "Create a concise summary of content",
            "analyze_claims": "Analyze and evaluate claims made in content",
            "create_markmap": "Generate a markmap visualization of content",
            "explain_code": "Explain what code does in plain language",
            "improve_writing": "Enhance and improve written content",
            "extract_article_wisdom": "Extract key insights from articles",
            "create_visualization": "Create visual representations of data/concepts",
            "answer_interview_question": "Help formulate answers to interview questions",
            "create_quiz": "Generate quiz questions from content",
        }

        return descriptions.get(pattern_name, f"Fabric AI pattern for {pattern_name.replace('_', ' ')}")

    async def _ensure_patterns_loaded(self):
        """Ensure patterns list is loaded."""
        if not self.patterns_list:
            await self._load_patterns_list()

    async def _load_patterns_list(self):
        """Load the list of available patterns from GitHub."""
        cache_file = self.cache_dir / "patterns_list.json"
        cache_meta_file = self.cache_dir / "patterns_list_meta.json"

        # Check if we should update from GitHub
        should_fetch = True
        cached_patterns = []

        if cache_file.exists() and cache_meta_file.exists():
            try:
                # Load cache metadata
                with open(cache_meta_file, 'r') as f:
                    meta = json.load(f)
                    cache_age_hours = (time.time() - meta.get('timestamp', 0)) / 3600

                # Load cached patterns
                with open(cache_file, 'r') as f:
                    cached_patterns = json.load(f)

                # Check if cache is still fresh
                if AUTO_UPDATE and cache_age_hours < CACHE_TTL_HOURS:
                    should_fetch = False
                    self.patterns_list = cached_patterns
                    logger.info(f"Loaded {len(self.patterns_list)} patterns from cache (age: {cache_age_hours:.1f}h)")
                elif AUTO_UPDATE:
                    logger.info(f"Cache expired ({cache_age_hours:.1f}h old), checking for updates...")
                else:
                    should_fetch = False
                    self.patterns_list = cached_patterns
                    logger.info(f"Loaded {len(self.patterns_list)} patterns from cache (auto-update disabled)")

            except Exception as e:
                logger.warning(f"Error reading cache: {e}, will fetch from GitHub")
                should_fetch = True

        if should_fetch:
            try:
                # Fetch from GitHub API
                logger.info("Fetching latest patterns from GitHub...")
                url = f"{GITHUB_API_BASE}/repos/{FABRIC_REPO}/contents/{PATTERNS_PATH}"
                response = await self.http_client.get(url)
                response.raise_for_status()

                items = response.json()
                new_patterns = [item["name"] for item in items if item["type"] == "dir"]

                # Check if there are any changes
                if cached_patterns and set(new_patterns) != set(cached_patterns):
                    added = set(new_patterns) - set(cached_patterns)
                    removed = set(cached_patterns) - set(new_patterns)
                    if added:
                        logger.info(f"✨ New patterns available: {', '.join(sorted(added))}")
                    if removed:
                        logger.info(f"⚠️  Patterns removed: {', '.join(sorted(removed))}")
                    logger.info(f"Updated from {len(cached_patterns)} to {len(new_patterns)} patterns")
                elif cached_patterns:
                    logger.info(f"Patterns are up to date ({len(new_patterns)} patterns)")
                else:
                    logger.info(f"Downloaded {len(new_patterns)} patterns")

                self.patterns_list = new_patterns

                # Save to cache with metadata
                with open(cache_file, 'w') as f:
                    json.dump(self.patterns_list, f)

                with open(cache_meta_file, 'w') as f:
                    json.dump({
                        'timestamp': time.time(),
                        'count': len(self.patterns_list),
                        'version': FABRIC_BRANCH
                    }, f)

            except Exception as e:
                logger.error(f"Error fetching patterns from GitHub: {e}")
                # Fall back to cache if available
                if cached_patterns:
                    self.patterns_list = cached_patterns
                    logger.info(f"Using cached patterns ({len(cached_patterns)} patterns)")
                else:
                    # Use a minimal fallback list
                    self.patterns_list = ["extract_wisdom", "summarize", "analyze_claims"]
                    logger.warning(f"Using minimal fallback pattern list")

    async def _get_pattern(self, pattern_name: str) -> str:
        """Get the content of a specific pattern."""
        # Check cache
        if pattern_name in self.patterns_cache:
            return self.patterns_cache[pattern_name]

        # Try to load from file cache
        cache_file = self.cache_dir / f"{pattern_name}.md"
        if cache_file.exists():
            content = cache_file.read_text(encoding='utf-8')
            self.patterns_cache[pattern_name] = content
            return content

        # Fetch from GitHub
        try:
            url = f"{GITHUB_RAW_BASE}/{FABRIC_REPO}/{FABRIC_BRANCH}/{PATTERNS_PATH}/{pattern_name}/system.md"
            response = await self.http_client.get(url)
            response.raise_for_status()

            content = response.text

            # Cache it
            self.patterns_cache[pattern_name] = content
            cache_file.write_text(content, encoding='utf-8')

            logger.info(f"Fetched pattern: {pattern_name}")
            return content

        except Exception as e:
            logger.error(f"Error fetching pattern {pattern_name}: {e}")
            return f"# Error loading pattern: {pattern_name}\n\nCould not fetch pattern from GitHub."

    async def run(self):
        """Run the MCP server."""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


def main():
    """Main entry point."""
    server = FabricMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
