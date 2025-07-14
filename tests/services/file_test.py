from pathlib import Path

import pytest

from src.services.file import File


def test_file_txt(tmp_path: Path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("hello world")

    file = File(file_path).get_file()

    assert isinstance(file, list)
    assert file[0]["path"] == str(file_path)
    assert file[0]["file_name"] == "test_file.txt"
    assert file[0]["extension"] == ".txt"
    assert file[0]["text"] == "hello world"
    assert isinstance(file[0]["chunks"], str)


def test_file_md(tmp_path: Path):
    file_path = tmp_path / "test_file.md"
    file_path.write_text("hello world")

    file = File(file_path).get_file()

    assert isinstance(file, list)
    assert file[0]["path"] == str(file_path)
    assert file[0]["file_name"] == "test_file.md"
    assert file[0]["extension"] == ".md"
    assert file[0]["text"] == "hello world"
    assert isinstance(file[0]["chunks"], str)


@pytest.mark.skipif(
    not Path("tests/assets/test_file.pdf").exists(),
    reason="'test_file.pdf' not found for test",
)
def test_file_pdf(tmp_path: Path):
    file_path = tmp_path / "test_file.pdf"

    file = File(file_path).get_file()

    assert isinstance(file, list)
    assert file[0]["path"] == str(file_path)
    assert file[0]["extension"] == ".pdf"
    assert isinstance(file[0]["text"], str)
    assert isinstance(file[0]["chunks"], str)


def test_file_invalid_path():
    file_path = Path("/invalid_path/invalid.txt")
    file = File(file_path).get_file()

    assert isinstance(file, list)
    assert len(file) == 0
