# TackOnMCP
# File Management MCP Server

A lightweight, robust [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server built using Python and `FastMCP`. This server exposes file operation tools to AI assistants (like Claude Desktop or custom MCP clients), allowing them to safely create, read, append, list, and convert files.

---

## Features

- **Create Text Files**: Create `.txt` files with optional initial content and overwrite protection.
- **Read Files**: Inspect the contents of existing text/markdown/html files.
- **List Workspace Files**: View all managed files in the working directory.
- **Append Content**: Append formatted lines of text to existing `.txt` files.
- **Convert File Extensions**: Rename existing `.txt` files to `.html` or `.md` formats.
- **Secure Sandboxing**: Restricts file operations strictly to the server's working directory.

---

## Tools

### 1. `create_txt_file`
Creates a new file with a `.txt` extension.
- **Parameters**:
  - `filename` (`string`, required): Name of the file (e.g., `"notes"` or `"notes.txt"`).
  - `initial_content` (`string`, optional): Initial text content.
  - `overwrite` (`boolean`, optional): Whether to overwrite if the file exists (default `false`).

### 2. `read_file`
Reads and returns the content of a file.
- **Parameters**:
  - `filename` (`string`, required): Name of the file to read.

### 3. `append_to_txt_file`
Appends a line of text to an existing `.txt` file.
- **Parameters**:
  - `filename` (`string`, required): Name of the file.
  - `line` (`string`, required): Text line to append with a trailing newline.

### 4. `list_files`
Lists all managed text, markdown, and html files in the workspace.

### 5. `change_file_extension`
Changes the file extension of a `.txt` file to `.html` or `.md`.
- **Parameters**:
  - `filename` (`string`, required): Target file name.
  - `new_extension` (`string`, required): The target extension (`".html"` or `".md"`).

---

## Installation & Setup

1. **Ensure dependencies are installed**:
   ```bash
   pip install mcp
   ```

## Running the Tests
Install pytest (if you haven't already):

```bash
pip install pytest
```
Run the test suite:

```bash
pytest -v
```
