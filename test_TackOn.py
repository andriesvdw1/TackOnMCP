
import os
import sys
import pytest
from pathlib import Path

# Ensure TackOn.py can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent))

import TackOn


@pytest.fixture(autouse=True)
def setup_workspace(tmp_path, monkeypatch):
    """Give every test its own isolated workspace."""

    workspace = tmp_path.resolve()

    monkeypatch.chdir(workspace)
    monkeypatch.setattr(TackOn, "BASE_DIR", workspace)

    yield workspace


# -----------------------------------------
# FILE CREATION TESTS
# -----------------------------------------

def test_create_txt_file(setup_workspace):
    """Test creating a file with automatic .txt extension."""

    result = TackOn.create_txt_file("notes", "Hello MCP")

    assert "Success" in result

    path = setup_workspace / "notes.txt"

    assert path.exists()
    assert path.read_text(encoding="utf-8") == "Hello MCP"


def test_create_markdown_file(setup_workspace):
    """Test creating a Markdown file."""

    result = TackOn.create_txt_file("document.md", "# Hello")

    assert "Success" in result
    assert (setup_workspace / "document.md").exists()


def test_create_html_file(setup_workspace):
    """Test creating an HTML file."""

    result = TackOn.create_txt_file(
        "index.html",
        "<h1>Hello World</h1>"
    )

    assert "Success" in result
    assert (setup_workspace / "index.html").exists()


def test_unsupported_extension(setup_workspace):
    """Test that unsupported extensions receive .txt."""

    result = TackOn.create_txt_file("notes.exe", "Test")

    assert "Success" in result
    assert (setup_workspace / "notes.exe.txt").exists()


def test_create_nested_directory(setup_workspace):
    """Test creating a file inside a new directory."""

    result = TackOn.create_txt_file(
        "documents/notes.txt",
        "Nested content"
    )

    assert "Success" in result
    assert (
        setup_workspace / "documents" / "notes.txt"
    ).exists()


# -----------------------------------------
# OVERWRITE PROTECTION TESTS
# -----------------------------------------

def test_create_file_overwrite_protection(setup_workspace):
    """Test that existing files are protected."""

    TackOn.create_txt_file("data.txt", "Initial")

    # Attempt overwrite without permission
    res_fail = TackOn.create_txt_file(
        "data.txt",
        "New",
        overwrite=False
    )

    assert "Error" in res_fail
    assert TackOn.read_file("data.txt") == "Initial"

    # Attempt overwrite with permission
    res_success = TackOn.create_txt_file(
        "data.txt",
        "New",
        overwrite=True
    )

    assert "Success" in res_success
    assert TackOn.read_file("data.txt") == "New"


# -----------------------------------------
# FILE READING TESTS
# -----------------------------------------

def test_read_file(setup_workspace):
    """Test reading existing and missing files."""

    TackOn.create_txt_file(
        "story.txt",
        "Once upon a time..."
    )

    content = TackOn.read_file("story.txt")

    assert content == "Once upon a time..."

    error_res = TackOn.read_file("nonexistent.txt")

    assert "Error" in error_res


# -----------------------------------------
# FILE APPENDING TESTS
# -----------------------------------------

def test_append_to_txt_file(setup_workspace):
    """Test appending text with a newline."""

    TackOn.create_txt_file(
        "todo.txt",
        "Task 1\n"
    )

    result = TackOn.append_to_txt_file(
        "todo.txt",
        "Task 2"
    )

    assert "Success" in result

    content = TackOn.read_file("todo.txt")

    assert content == "Task 1\nTask 2\n"


def test_append_to_missing_file():
    """Test that appending to missing files fails."""

    result = TackOn.append_to_txt_file(
        "missing.txt",
        "New task"
    )

    assert "Error" in result


# -----------------------------------------
# FILE LISTING TESTS
# -----------------------------------------

def test_list_files(setup_workspace):
    """Test listing supported files."""

    TackOn.create_txt_file("doc1.txt", "Text")
    TackOn.create_txt_file("doc2.md", "Markdown")
    TackOn.create_txt_file("doc3.html", "HTML")

    listing = TackOn.list_files()

    assert "doc1.txt" in listing
    assert "doc2.md" in listing
    assert "doc3.html" in listing


def test_list_files_empty():
    """Test listing an empty workspace."""

    result = TackOn.list_files()

    assert "No managed files" in result


def test_list_files_ignores_subdirectories(setup_workspace):
    """Test that only root directory files are listed."""

    TackOn.create_txt_file(
        "documents/hidden.txt",
        "Nested file"
    )

    result = TackOn.list_files()

    assert "hidden.txt" not in result


# -----------------------------------------
# EXTENSION CHANGE TESTS
# -----------------------------------------

def test_change_file_extension(setup_workspace):
    """Test changing .txt to .html."""

    TackOn.create_txt_file(
        "page.txt",
        "<h1>Hello</h1>"
    )

    result = TackOn.change_file_extension(
        "page.txt",
        ".html"
    )

    assert "Success" in result

    assert not (setup_workspace / "page.txt").exists()
    assert (setup_workspace / "page.html").exists()

    assert TackOn.read_file("page.html") == "<h1>Hello</h1>"


def test_change_file_extension_invalid():
    """Test rejection of unsupported target extensions."""

    TackOn.create_txt_file("page.txt", "Text")

    result = TackOn.change_file_extension(
        "page.txt",
        "exe"
    )

    assert "Error" in result


def test_change_file_extension_destination_exists(
    setup_workspace
):
    """Test protection against replacing an existing destination."""

    TackOn.create_txt_file("page.txt", "Original")
    TackOn.create_txt_file("page.md", "Existing")

    result = TackOn.change_file_extension(
        "page.txt",
        ".md"
    )

    assert "Error" in result

    assert TackOn.read_file("page.txt") == "Original"
    assert TackOn.read_file("page.md") == "Existing"


def test_change_to_same_extension():
    """Test changing a file to its current extension."""

    TackOn.create_txt_file("page.md", "Markdown")

    result = TackOn.change_file_extension(
        "page.md",
        ".md"
    )

    assert "already has that extension" in result


# -----------------------------------------
# SECURITY TESTS
# -----------------------------------------

def test_security_path_traversal():
    """Test that directory traversal is blocked."""

    with pytest.raises(ValueError, match="Security Error"):
        TackOn._get_safe_path("../outside.txt")


def test_security_absolute_path(setup_workspace):
    """Test that absolute paths outside the workspace are blocked."""

    outside_path = setup_workspace.parent / "outside.txt"

    with pytest.raises(ValueError, match="Security Error"):
        TackOn._get_safe_path(str(outside_path))


def test_security_empty_filename():
    """Test that empty filenames are rejected."""

    with pytest.raises(ValueError, match="Filename cannot be empty"):
        TackOn._get_safe_path("")


def test_security_symbolic_link(setup_workspace):
    """Test that symbolic links cannot access outside files."""

    outside_file = setup_workspace.parent / "outside.txt"
    outside_file.write_text("Secret", encoding="utf-8")

    link = setup_workspace / "escape.txt"

    try:
        link.symlink_to(outside_file)
    except (OSError, NotImplementedError):
        pytest.skip("Symbolic links are unavailable on this system.")

    with pytest.raises(ValueError, match="Security Error"):
        TackOn._get_safe_path("escape.txt")
