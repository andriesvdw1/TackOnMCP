# TackOnMCP
# File Management MCP Server

A lightweight, robust [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server built using Python and `FastMCP`. This server exposes file operation tools to AI assistants (like Claude Desktop or custom MCP clients), allowing them to safely create `.txt` files, append lines to existing files, and convert `.txt` files to `.md` or `.html` formats.

---

## Features

- **Create Text Files**: Create `.txt` files with optional initial content.
- **Append Content**: Append formatted lines of text to existing `.txt` files.
- **Convert File Extensions**: Rename existing `.txt` files to `.html` or `.md` formats with strict validation.
- **FastMCP Framework**: Uses the standard python `mcp` library for standard I/O (stdio) communication.

---

## Tools

The server registers three primary tools available for MCP clients:

### 1. `create_txt_file`
Creates a new file with a `.txt` extension.
- **Parameters**:
  - `filename` (`string`, required): Name of the file (e.g., `"notes"` or `"notes.txt"`).
  - `initial_content` (`string`, optional): Initial text content to populate the file.
- **Behavior**: Automatically appends `.txt` if omitted. Writes content in UTF-8.

### 2. `append_to_txt_file`
Appends a line of text to an existing `.txt` file.
- **Parameters**:
  - `filename` (`string`, required): Name of the existing `.txt` file.
  - `line` (`string`, required): Text line to append to the end of the file.
- **Behavior**: Ensures the file exists before appending and automatically includes a trailing newline character (`\n`).

### 3. `change_file_extension`
Changes the file extension of a `.txt` file to `.html` or `.md`.
- **Parameters**:
  - `filename` (`string`, required): Target file name ending in `.txt`.
  - `new_extension` (`string`, required): The target extension (`".html"`, `".md"`, `"html"`, or `"md"`).
- **Behavior**: Validates that the file exists, checks that the target extension is valid, and renames the file using `os.rename`.

---

## Prerequisites

- Python 3.10 or higher
- `mcp` SDK

---

## Installation & Setup

1. **Clone or download this repository** containing `file_server.py`.
2. **Install dependencies**:
   ```bash
   pip install mcp
   ```

3. **Verify locally**:
   You can verify that the script runs without syntax errors:
   ```bash
   python file_server.py
   ```
   *(Note: The server runs via standard input/output (stdio), so running it directly in terminal will wait for MCP JSON-RPC input).*

---

## Configuration & Usage

### Integrating with Claude Desktop

Add the server configuration to your `claude_desktop_config.json`:

- **MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "file-manager": {
      "command": "python",
      "args": [
        "/path/to/your/file_server.py"
      ]
    }
  }
}
```

*Note: Replace `/path/to/your/file_server.py` with the full absolute path to where `file_server.py` is saved on your system.*

---

## Example Prompts for AI Client

Once connected, you can interact with the tools using natural language commands:

- **Create a file**: *"Create a text file called meeting_notes with the title 'Project Kickoff'."*
- **Append text**: *"Add 'Action item: Draft initial proposal by Friday' to meeting_notes.txt."*
- **Convert extension**: *"Convert meeting_notes.txt into a Markdown file."*

---

## Error Handling

The server returns clear error messages for common file system edge cases:
- Missing files during append or rename operations.
- Attempting to convert files with extensions other than `.txt`.
- Attempting to rename files to unsupported target extensions (only `.html` and `.md` are permitted).
- OS permission and read/write exceptions.

---

