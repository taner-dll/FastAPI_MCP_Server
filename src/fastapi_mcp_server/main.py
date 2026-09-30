from fastapi import FastAPI
from .mcp_server import mcp
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager


# Create a streamable HTTP app for the MCP server
mcp_app = mcp.streamable_http_app(
    streamable_http_path="/"
)

# Define the lifespan context manager for the FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with mcp.session_manager.run():
        yield


app = FastAPI(
    title="FastAPI MCP Server",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}



app.mount("/mcp", mcp_app, name="mcp")


    