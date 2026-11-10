# TackOnMCP

A Python-based [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server for managing files through AI assistants and MCP-compatible clients.

Built with Python and FastMCP, TackOn provides tools for creating, reading, appending, listing, and renaming files within a designated workspace.

## Features

- **Create files:** Create `.txt`, `.md`, and `.html` files with optional initial content.
- **Overwrite protection:** Existing files cannot be overwritten unless explicitly permitted.
- **Read files:** Read the contents of supported files.
- **Append content:** Append text to existing files.
- **List files:** List supported files in the workspace root directory.
- **Change extensions:** Rename files to `.html` or `.md`.
- **Workspace protection:** Restrict file access to the configured workspace directory.
- **Path validation:** Reject directory traversal and symbolic links that resolve outside the workspace.

## Available MCP Tools

TackOn exposes five tools to connected MCP clients.

### 1. `create_txt_file`

Creates a new file with optional initial content.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `filename` | string | Yes | — | File name or relative path |
| `initial_content` | string | No | `""` | Initial file contents |
| `overwrite` | boolean | No | `false` | Allow replacing an existing file |

**Supported extensions:** `.txt`, `.md`, `.html`

If no supported extension is provided, `.txt` is automatically appended.

Examples:

- `notes` → `notes.txt`
- `notes.txt` → `notes.txt`
- `document.md` → `document.md`
- `index.html` → `index.html`
- `report.pdf` → `report.pdf.txt`

Files in new subdirectories can also be created.

### 2. `read_file`

Reads and returns the contents of an existing file.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `filename` | string | Yes | File name or relative path |

Supports `.txt`, `.md`, and `.html` files.

Returns the file contents or an error message if the file cannot be read.

### 3. `append_to_txt_file`

Appends text to an existing file.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `filename` | string | Yes | File name or relative path |
| `line` | string | Yes | Text to append |

A newline character is automatically added after the appended text.

The file must already exist.

### 4. `list_files`

Lists supported files in the workspace root directory.

No parameters are required.

The listing includes:

- `.txt`
- `.md`
- `.html`

Files inside subdirectories are not included.

### 5. `change_file_extension`

Renames an existing file by changing its extension.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `filename` | string | Yes | Existing file name or relative path |
| `new_extension` | string | Yes | Target extension |

Allowed target extensions:

- `.html`
- `.md`

The operation preserves the original file contents and refuses to rename the file if the destination already exists.

## Installation

### Requirements

- Python 3.9 or newer
- pip
- An MCP-compatible client
- FastMCP (provided by the `mcp` Python package)

### 1. Clone or download the project

```bash
git clone <repository-url>
cd TackOnMCP
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install mcp
```

### 4. Start the server

```bash
python TackOn.py
```

The server uses MCP's standard input/output (stdio) transport.

It is intended to be launched by an MCP-compatible client rather than operated as a standalone HTTP server.

## Workspace Configuration

TackOn uses the directory from which the server process is launched as its workspace.

The workspace is determined by:

```python
BASE_DIR = Path.cwd().resolve()
```

For example, if the server is launched from:

```text
C:\Users\Admin\TackOnWorkspace
```

That directory becomes the workspace for file operations.

Files can be created inside subdirectories, provided those directories remain within the workspace.

**Important:** Launch the server with the intended workspace as its working directory. The workspace is not automatically set to the location of `TackOn.py`.

## Security

TackOn includes basic filesystem protections:

- Resolves paths before accessing files.
- Rejects paths outside the workspace.
- Checks resolved paths to prevent directory traversal.
- Rejects symbolic links that resolve outside the workspace.
- Prevents accidental overwriting during normal file creation.
- Prevents extension changes from replacing existing destination files.

The workspace restriction is an application-level safeguard, not a complete operating-system security boundary. For stronger isolation, run the server under a dedicated operating-system account with appropriate filesystem permissions.

Only connect trusted MCP clients, since connected AI assistants can request file operations within the workspace.

## Running the Tests

TackOn includes a pytest test suite covering file operations, extension handling, overwrite protection, and path validation.

### 1. Install pytest

```bash
python -m pip install pytest
```

### 2. Run the tests

From the project directory:

```bash
python -m pytest -v
```

The tests use temporary directories to isolate file operations and avoid modifying your actual workspace.

Symbolic-link tests may be skipped if the operating system does not permit symbolic-link creation.

## Project Structure

```text
TackOnMCP/
│
├── TackOn.py
├── test_tackon.py
├── README.md
│
└── .venv/
```

## License

Specify your preferred open-source license here before distributing the project.
