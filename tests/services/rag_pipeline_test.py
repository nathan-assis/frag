from pathlib import Path

import pytest
from fastapi import HTTPException

from src.services.rag_pipeline import RAGPipeline


def test_set_folder_with_valid_folder(tmp_path: Path):
    RAGPipeline._RAGPipeline__folder = None

    files = [Path(tmp_path / "file1.txt"), Path(tmp_path / "file2.md")]
    (files[0]).write_text("hello world")
    (files[1]).write_text("hello world")

    RAGPipeline._RAGPipeline__set_folder(str(tmp_path))
    folder = RAGPipeline._RAGPipeline__folder

    assert folder is not None
    assert folder.path == tmp_path
    assert files == folder.files
    assert len(folder.files) == 2


def test_set_folder_with_empty_folder(tmp_path: Path):
    RAGPipeline._RAGPipeline__folder = None

    RAGPipeline._RAGPipeline__set_folder(str(tmp_path))
    folder = RAGPipeline._RAGPipeline__folder

    assert folder is not None
    assert folder.path == tmp_path
    assert folder.files == []


def test_set_folder_with_nonexistent_folder():
    RAGPipeline._RAGPipeline__folder = None

    with pytest.raises(HTTPException) as e:
        RAGPipeline._RAGPipeline__set_folder("/non/existent")

    assert e.value.status_code == 400
    assert "Invalid path" in e.value.detail


def test_set_folder_with_file(tmp_path: Path):
    RAGPipeline._RAGPipeline__folder = None

    file_path = tmp_path / "file.txt"
    file_path.write_text("hello world")

    with pytest.raises(HTTPException) as e:
        RAGPipeline._RAGPipeline__set_folder(str(file_path))

    assert e.value.status_code == 400
    assert "Invalid path" in e.value.detail
