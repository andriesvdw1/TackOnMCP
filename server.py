
from pathlib import Path
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("TackOnMCP")

@mcp.tool()
def create_file(filename: str) -> str:
    """Create an empty .txt TEXT FILE, never a folder.
    Example input: filename='hello.txt'
    The filename must end in .txt.
    """
    base_dir = Path(__file__).resolve().parent

    # Reject folder paths and names without a .txt extension.
    if not filename.lower().endswith(".txt"):
        return "Error: Provide a filename ending in .txt, such as hello.txt."

    if Path(filename).name != filename or filename in (".", ".."):
        return "Error: Provide only a filename, not a folder path."

    target = base_dir / filename

    if target.exists():
        return f"Error: A file or folder named {filename} already exists."

    target.touch()

    if not target.is_file():
        return "Error: The target was not created as a file."

    return f"Success: Created an empty text file named {filename}."

if __name__ == "__main__":
    mcp.run(transport="stdio")
