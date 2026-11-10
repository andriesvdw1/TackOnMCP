import os
from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("TackOn File Management Server")

# Define a secure workspace directory to prevent path traversal attacks
BASE_DIR = os.path.abspath(os.getcwd())

def _get_safe_path(filename: str) -> str:
    """Resolve and validate that the path stays safely within the base directory."""
    # Ensure default extension if none provided
    if not filename.endswith((".txt", ".md", ".html")):
        if not filename.endswith(".txt"):
            filename += ".txt"
    
    path = os.path.abspath(os.path.join(BASE_DIR, filename))
    
    # Ensure the resolved path is strictly inside BASE_DIR
    if os.path.commonpath([BASE_DIR, path]) != BASE_DIR:
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
        filename_only = os.path.basename(path)
        
        if os.path.exists(path) and not overwrite:
            return f"Error: File '{filename_only}' already exists. Set overwrite=True to overwrite."
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(initial_content)
            
        return f"Success: File '{filename_only}' was created successfully."
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
        filename_only = os.path.basename(path)
        
        if not os.path.exists(path):
            return f"Error: File '{filename_only}' does not exist."
            
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
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
        filename_only = os.path.basename(path)
        
        if not os.path.exists(path):
            return f"Error: File '{filename_only}' does not exist. Please create it first."
        
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        return f"Success: Line appended to '{filename_only}'."
    except Exception as e:
        return f"Error appending to file: {str(e)}"


@mcp.tool()
def list_files() -> str:
    """List all managed text, markdown, and html files in the workspace directory."""
    try:
        files = []
        for entry in os.listdir(BASE_DIR):
            full_path = os.path.join(BASE_DIR, entry)
            if os.path.isfile(full_path) and entry.lower().endswith((".txt", ".md", ".html")):
                files.append(entry)
                
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
        filename_only = os.path.basename(path)
        
        if not os.path.exists(path):
            return f"Error: File '{filename_only}' does not exist."

        base_name, _ = os.path.splitext(path)
        new_path = base_name + new_extension
        new_filename_only = os.path.basename(new_path)
        
        os.rename(path, new_path)
        return f"Success: Changed file extension from '{filename_only}' to '{new_filename_only}'."
    except Exception as e:
        return f"Error renaming file: {str(e)}"


if __name__ == "__main__":
    # Run the server using stdio transport for MCP clients
    mcp.run()
