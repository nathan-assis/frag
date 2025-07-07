from pathlib import Path

import pytest

from src.services.file import File


def test_file_txt(tmp_path: Path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("hello world")

    file = File(file_path).get_file()

    assert file["path"] == file_path
    assert file["file_name"] == "test_file.txt"
    assert file["extension"] == ".txt"
    assert file["text"] == "hello world"
    assert isinstance(file["chunks"], list)


def test_file_md(tmp_path: Path):
    file_path = tmp_path / "test_file.md"
    file_path.write_text("hello world")

    file = File(file_path).get_file()

    assert file["path"] == file_path
    assert file["file_name"] == "test_file.md"
    assert file["extension"] == ".md"
    assert file["text"] == "hello world"
    assert isinstance(file["chunks"], list)


@pytest.mark.skipif(
    not Path("tests/assets/test_file.pdf").exists(),
    reason="'test_file.pdf' not found for test",
)
def test_file_pdf(tmp_path: Path):
    file_path = tmp_path / "test_file.pdf"

    file = File(file_path).get_file()

    assert file["path"] == file_path
    assert file["extension"] == ".pdf"
    assert isinstance(file["text"], str)
    assert isinstance(file["chunks"], list)


def test_file_invalid_path():
    file_path = Path("/invalid_path/invalid.txt")
    file = File(file_path).get_file()

    assert file["path"] is None
    assert file["extension"] is None
    assert file["text"] is None
    assert file["chunks"] == []
    assert file["embeddings"] == []
