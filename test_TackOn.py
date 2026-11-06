import os
from pathlib import Path
import pytest
import TackOn

@pytest.fixture(autouse=True)
def setup_workspace(tmp_path, monkeypatch):
    """Isolate the workspace directory for each test using a temporary folder."""
    monkeypatch.chdir(tmp_path)
    # Redirect TackOn's BASE_DIR to the temporary directory path
    monkeypatch.setattr(TackOn, "BASE_DIR", tmp_path.resolve())
    yield tmp_path


def test_create_txt_file():
    """Test creating a new text file with automatic .txt extension handling."""
    result = TackOn.create_txt_file("notes", "Hello MCP")
    assert "Success" in result
    
    path = TackOn.BASE_DIR / "notes.txt"
    assert path.exists()
    assert path.read_text(encoding="utf-8") == "Hello MCP"


def test_create_file_overwrite_protection():
    """Test that files cannot be accidentally overwritten unless specified."""
    TackOn.create_txt_file("data.txt", "Initial")
    
    # Attempt overwrite without flag (should fail)
    res_fail = TackOn.create_txt_file("data.txt", "New", overwrite=False)
    assert "Error" in res_fail
    assert TackOn.read_file("data.txt") == "Initial"
    
    # Attempt overwrite with flag (should succeed)
    res_success = TackOn.create_txt_file("data.txt", "New", overwrite=True)
    assert "Success" in res_success
    assert TackOn.read_file("data.txt") == "New"


def test_read_file():
    """Test reading existing and non-existing files."""
    TackOn.create_txt_file("story.txt", "Once upon a time...")
    
    content = TackOn.read_file("story.txt")
    assert content == "Once upon a time..."
    
    # Read missing file
    error_res = TackOn.read_file("nonexistent.txt")
    assert "Error" in error_res


def test_append_to_txt_file():
    """Test appending lines with trailing newlines to text files."""
    TackOn.create_txt_file("todo.txt", "Task 1\n")
    
    res = TackOn.append_to_txt_file("todo.txt", "Task 2")
    assert "Success" in res
    
    content = TackOn.read_file("todo.txt")
    assert content == "Task 1\nTask 2\n"


def test_list_files():
    """Test listing managed files in the workspace."""
    TackOn.create_txt_file("doc1.txt", "text")
    TackOn.create_txt_file("doc2.md", "markdown")
    
    listing = TackOn.list_files()
    assert "doc1.txt" in listing
    assert "doc2.md" in listing


def test_change_file_extension():
    """Test successfully changing extensions between .txt, .md, and .html."""
    TackOn.create_txt_file("page.txt", "<h1>Hello</h1>")
    
    res = TackOn.change_file_extension("page.txt", ".html")
    assert "Success" in res
    
    assert not (TackOn.BASE_DIR / "page.txt").exists()
    assert (TackOn.BASE_DIR / "page.html").exists()
    assert TackOn.read_file("page.html") == "<h1>Hello</h1>"


def test_change_file_extension_invalid():
    """Test that invalid target extensions are rejected."""
    TackOn.create_txt_file("page.txt", "text")
    
    res = TackOn.change_file_extension("page.txt", "exe")
    assert "Error" in res


def test_security_path_traversal():
    """Test that directory traversal attempts are safely blocked."""
    with pytest.raises(ValueError, match="Security Error"):
        TackOn._get_safe_path("../outside.txt")
