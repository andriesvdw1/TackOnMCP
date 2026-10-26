from mcp.server.fastmcp import FastMCP
from pathlib import Path
mcp =FastMCP("TackOnMCP")
@mcp.tool()
def createFile():
    """Create a new empty file."""
    Path("File.txt").touch()
    return "Text file created successfully."
