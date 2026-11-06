import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("TackOn File Management Server")

# Define a secure workspace directory to prevent path traversal attacks
BASE_DIR = Path(os.getcwd()).resolve()

def _get_safe_path(filename: str) -> Path:
    """Resolve and validate that the path stays safely within the base directory."""
    # Ensure default .txt extension if none provided
    if not filename.endswith((".txt", ".md", ".html")):
        if not filename.endswith(".txt"):
            filename += ".txt"
    
    path = (BASE_DIR / filename).resolve()
    if not path.is_relative_to(BASE_DIR):
        raise ValueError("Security Error: Path traversal outside the working directory is not allowed.")
    return path


@mcp.tool()
def create_txt_file(filename: str, initial_content: str = "", overwrite: bool = False) -> str:
    """Create a new file with a .txt extension and optional initial content.

    Args:
        filename: The name of the file (e.g., 'notes' or 'notes.txt').
        initial_content: Optional text to write into the file initially.
        overwrite: Whether to overwrite the file if it already exists.
    """
    try:
        path = _get_safe_path(filename)
        if path.exists() and not overwrite:
            return f"Error: File '{path.name}' already exists. Set overwrite=True to overwrite."
        
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(initial_content, encoding="utf-8")
        return f"Success: File '{path.name}' was created successfully."
    except Exception as e:
        return f"Error creating file: {str(e)}"


@mcp.tool()
def read_file(filename: str) -> str:
    """Read and return the contents of a file in the workspace.

    Args:
        filename: The name of the file to read.
    """
    try:
        path = _get_safe_path(filename)
        if not path.exists():
            return f"Error: File '{path.name}' does not exist."
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {str(e)}"


@mcp.tool()
def append_to_txt_file(filename: str, line: str) -> str:
    """Append a line of text to an existing .txt file.

    Args:
        filename: The name of the file to append to.
        line: The line of text to append.
    """
    try:
        path = _get_safe_path(filename)
        if not path.exists():
            return f"Error: File '{path.name}' does not exist. Please create it first."
        
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        return f"Success: Line appended to '{path.name}'."
    except Exception as e:
        return f"Error appending to file: {str(e)}"


@mcp.tool()
def list_files() -> str:
    """List all managed text, markdown, and html files in the workspace directory."""
    try:
        files = [f.name for f in BASE_DIR.iterdir() if f.is_file() and f.suffix in (".txt", ".md", ".html")]
        if not files:
            return "No managed files found in the workspace."
        return "Workspace files:\n" + "\n".join(f"- {f}" for f in files)
    except Exception as e:
        return f"Error listing files: {str(e)}"


@mcp.tool()
def change_file_extension(filename: str, new_extension: str) -> str:
    """Change the file extension of a given file to either .html or .md.

    Args:
        filename: The current filename.
        new_extension: The target extension, either '.html' or '.md' (or 'html' / 'md').
    """
    if not new_extension.startswith("."):
        new_extension = "." + new_extension

    if new_extension not in [".html", ".md"]:
        return "Error: Invalid extension. Allowed target extensions are '.html' or '.md'."

    try:
        path = _get_safe_path(filename)
        if not path.exists():
            return f"Error: File '{path.name}' does not exist."

        new_path = path.with_suffix(new_extension)
        path.rename(new_path)
        return f"Success: Changed file extension from '{path.name}' to '{new_path.name}'."
    except Exception as e:
        return f"Error renaming file: {str(e)}"


if __name__ == "__main__":
    # Run the server using stdio transport for MCP clients
    mcp.run()
