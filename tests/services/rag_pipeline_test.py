from pathlib import Path

import pytest
from fastapi import HTTPException

from src.services.rag_pipeline import RAGPipeline


def test_validate_folder_with_valid_folder(tmp_path: Path):
    result = RAGPipeline._RAGPipeline__validate_folder(str(tmp_path))
    assert result == tmp_path


def test_validate_folder_with_nonexistent_folder():
    with pytest.raises(HTTPException) as e:
        RAGPipeline._RAGPipeline__validate_folder("/non/existent")

    assert e.value.status_code == 400
    assert "Caminho inválido" in e.value.detail


def test_validate_folder_with_file(tmp_path: Path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("hello world")

    with pytest.raises(HTTPException) as e:
        RAGPipeline._RAGPipeline__validate_folder(str(file_path))

    assert e.value.status_code == 400
    assert "Caminho inválido" in e.value.detail
