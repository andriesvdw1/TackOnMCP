import os
from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("File Management Server")


@mcp.tool()
def create_txt_file(filename: str, initial_content: str = "") -> str:
  """Create a new file with a .txt extension and optional initial content.

  Args:
      filename: The name of the file (e.g., 'notes' or 'notes.txt').
      initial_content: Optional text to write into the file initially.
  """
  # Ensure the filename ends with .txt
  if not filename.endswith(".txt"):
    filename += ".txt"

  try:
    with open(filename, "w", encoding="utf-8") as f:
      f.write(initial_content)
    return f"Success: File '{filename}' was created successfully."
  except Exception as e:
    return f"Error creating file: {str(e)}"


@mcp.tool()
def append_to_txt_file(filename: str, line: str) -> str:
  """Append a line of text to an existing .txt file.

  Args:
      filename: The name of the file to append to.
      line: The line of text to append.
  """
  if not filename.endswith(".txt"):
    filename += ".txt"

  if not os.path.exists(filename):
    return (
        f"Error: File '{filename}' does not exist. Please create it first."
    )

  try:
    with open(filename, "a", encoding="utf-8") as f:
      f.write(line + "\n")
    return f"Success: Line appended to '{filename}'."
  except Exception as e:
    return f"Error appending to file: {str(e)}"


@mcp.tool()
def change_file_extension(filename: str, new_extension: str) -> str:
  """Change the file extension of a given .txt file to either .html or .md.

  Args:
      filename: The current filename (must end in .txt).
      new_extension: The target extension, either '.html' or '.md' (or 'html' /
        'md').
  """
  # Clean up and normalize the target extension
  if not new_extension.startswith("."):
    new_extension = "." + new_extension

  if new_extension not in [".html", ".md"]:
    return (
        "Error: Invalid extension. Allowed target extensions are '.html' or"
        " '.md'."
    )

  if not filename.endswith(".txt"):
    return "Error: Source file must have a .txt extension."

  if not os.path.exists(filename):
    return f"Error: File '{filename}' does not exist."

  # Generate the new filename
  base_name = os.path.splitext(filename)[0]
  new_filename = base_name + new_extension

  try:
    os.rename(filename, new_filename)
    return (
        f"Success: Changed file extension from '{filename}' to '{new_filename}'."
    )
  except Exception as e:
    return f"Error renaming file: {str(e)}"


if __name__ == "__main__":
  # Run the server using stdio transport for MCP clients
  mcp.run()