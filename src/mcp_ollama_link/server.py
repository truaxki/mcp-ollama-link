import asyncio
import json

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio
from .query_ollama_qa import query_ollama  # Import from separate file

server = Server("mcp-ollama-link")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="query-ollama",
            description="Query the Ollama model with performance tracking",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The question or prompt to send to the model"
                    },
                    "context": {
                        "type": "string",
                        "description": "Additional context or background information for the query"
                    },
                    "model": {
                        "type": "string",
                        "default": "deepseek-r1:8b",
                        "description": 
                        """default: deepseek-r1:8b
                        Available models:
                        - deepseek-r1:32b (19 GB)
                        - deepseek-r1:7b (4.7 GB)
                        - deepseek-r1:8b (4.9 GB)
                        - deepseek-r1:1.5b (1.1 GB)
                        - llava-llama3 (5.5 GB)
                        - llava (4.7 GB)
                        - llama3.2-vision (7.9 GB)
                        - llama3.3 (42 GB)
                        - llama2 (3.8 GB)
                        - llama3.2 (2.0 GB)
                        The Ollama model to use for the query"""
                    }
                },
                "required": ["query", "context", "model"]
            },
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls."""
    if name == "query-ollama":
        try:
            if not arguments:
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps({"error": "Missing arguments"})
                    )
                ]

            query = arguments.get("query")
            context = arguments.get("context")
            model = arguments.get("model", "deepseek-r1:8b")

            if not all([query, context, model]):
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps({"error": "Missing required arguments"})
                    )
                ]
            
            full_prompt = f"Context: {context}\n\nQuery: {query}"
            response = await query_ollama(full_prompt, model)
            
            if response is None:
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps({"error": "Failed to get response from Ollama"})
                    )
                ]

            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({
                        "response": str(response),
                        "context": context,
                        "query": query
                    })
                )
            ]
        except Exception as e:
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)})
                )
            ]
    
    return [
        types.TextContent(
            type="text",
            text=json.dumps({"error": f"Unknown tool: {name}"})
        )
    ]


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-ollama-link",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )