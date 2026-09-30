from mcp.server import MCPServer

mcp = MCPServer("FastAPI_MCP_Server")

@mcp.tool()
def add(x: int, y: int) -> int:
    """ Add two numbers together."""    
    return x + y



