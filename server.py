
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("TackOn File Management Server")

# Secure workspace directory
BASE_DIR = Path.cwd().resolve()

ALLOWED_EXTENSIONS = {".txt", ".md", ".html"}


def _get_safe_path(filename: str) -> Path:
    """Resolve and validate a path inside the workspace."""

    if not filename or not filename.strip():
        raise ValueError("Filename cannot be empty.")

    # Add .txt if the extension isn't supported
    file_path = Path(filename)

    if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        file_path = Path(str(file_path) + ".txt")

    # Resolve absolute paths and symbolic links
    path = (BASE_DIR / file_path).resolve()

    # Prevent directory traversal
    if not path.is_relative_to(BASE_DIR) or path == BASE_DIR:
        raise ValueError(
            "Security Error: Access outside the workspace is prohibited."
        )

    return path


@mcp.tool()
def create_txt_file(
    filename: str,
    initial_content: str = "",
    overwrite: bool = False
) -> str:
    """Create a text, markdown or HTML file.

    Args:
        filename: Filename, e.g. notes or notes.txt.
        initial_content: Initial content to write.
        overwrite: Allow replacing an existing file.
    """
    try:
        path = _get_safe_path(filename)

        path.parent.mkdir(parents=True, exist_ok=True)

        # Revalidate after creating directories
        path = _get_safe_path(str(path))

        mode = "w" if overwrite else "x"

        with open(path, mode, encoding="utf-8") as f:
            f.write(initial_content)

        return f"Success: Created '{path.name}'."

    except FileExistsError:
        return f"Error: '{path.name}' already exists. Use overwrite=True."

    except Exception as e:
        return f"Error creating file: {str(e)}"


@mcp.tool()
def read_file(filename: str) -> str:
    """Read the contents of a workspace file.

    Args:
        filename: Name of the file to read.
    """
    try:
        path = _get_safe_path(filename)

        if not path.is_file():
            return f"Error: File '{path.name}' does not exist."

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    except Exception as e:
        return f"Error reading file: {str(e)}"


@mcp.tool()
def append_to_txt_file(filename: str, line: str) -> str:
    """Append text to an existing file.

    Args:
        filename: File to append to.
        line: Text to append.
    """
    try:
        path = _get_safe_path(filename)

        if not path.is_file():
            return f"Error: File '{path.name}' does not exist."

        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

        return f"Success: Text appended to '{path.name}'."

    except Exception as e:
        return f"Error appending to file: {str(e)}"


@mcp.tool()
def list_files() -> str:
    """List managed files in the workspace root directory."""
    try:
        files = []

        for entry in BASE_DIR.iterdir():
            if (
                entry.is_file()
                and not entry.is_symlink()
                and entry.suffix.lower() in ALLOWED_EXTENSIONS
            ):
                files.append(entry.name)

        if not files:
            return "No managed files found in the workspace."

        return "Workspace files:\n" + "\n".join(
            f"- {name}" for name in sorted(files)
        )

    except Exception as e:
        return f"Error listing files: {str(e)}"


@mcp.tool()
def change_file_extension(
    filename: str,
    new_extension: str
) -> str:
    """Change a file extension to .html or .md.

    Args:
        filename: Existing filename.
        new_extension: Target extension (.html or .md).
    """
    new_extension = new_extension.strip().lower()

    if not new_extension.startswith("."):
        new_extension = "." + new_extension

    if new_extension not in {".html", ".md"}:
        return "Error: Allowed extensions are .html and .md."

    try:
        path = _get_safe_path(filename)

        if not path.is_file():
            return f"Error: File '{path.name}' does not exist."

        new_path = path.with_suffix(new_extension)

        if new_path == path:
            return "The file already has that extension."

        if new_path.exists():
            return f"Error: Destination '{new_path.name}' already exists."

        new_path = _get_safe_path(str(new_path))

        path.rename(new_path)

        return (
            f"Success: Changed '{path.name}' "
            f"to '{new_path.name}'."
        )

    except Exception as e:
        return f"Error renaming file: {str(e)}"


if __name__ == "__main__":
    # Start MCP server using stdio transport
    mcp.run()
