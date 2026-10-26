from mcp.server.mcpserver import MCPServer
from pathlib import Path
mcp =MCPServer("TackOnMCP")
@mcp.tool()
def createFile():
    """Create a new empty file."""
    Path("File.txt").touch()
    return "Text file created successfully."

if __name__ == "__main__":
    mcp.run() # for use on local computers by default.