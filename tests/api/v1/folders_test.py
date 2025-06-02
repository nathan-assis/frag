import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from src.api import app
from src.api.v1.folders import validate_folder

client = TestClient(app)


def test_validate_folder_with_valid_folder():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = validate_folder(tmp_dir)
        assert isinstance(path, Path)
        assert path.exists()
        assert path.is_dir()


def test_validate_folder_with_non_existent_folder():
    caminho_fake = "/caminho/que/nao/existe"
    try:
        validate_folder(caminho_fake)
        raise AssertionError("Esperado HTTPException para caminho inexistente")
    except Exception as e:
        assert e.status_code == 400
        assert "Caminho não encontrado" in e.detail


def test_validate_folder_with_file():
    with tempfile.NamedTemporaryFile() as tmp_file:
        try:
            validate_folder(tmp_file.name)
            raise AssertionError("Esperado HTTPException para arquivo em vez de pasta")
        except Exception as e:
            assert e.status_code == 400
            assert "não é uma pasta" in e.detail


def test_receive_folder_com_sucesso():
    with tempfile.TemporaryDirectory() as tmp_dir:
        response = client.post("/api/v1/folders", json={"path": tmp_dir})
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert "registrada com sucesso" in response.json()["message"]


def test_receive_folder_com_pasta_inexistente():
    response = client.post("/api/v1/folders", json={"path": "/nao/existe"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Caminho não encontrado."


def test_receive_folder_com_arquivo_ao_invés_de_pasta():
    with tempfile.NamedTemporaryFile() as tmp_file:
        response = client.post("/api/v1/folders", json={"path": tmp_file.name})
        assert response.status_code == 400
        assert response.json()["detail"] == "O caminho informado não é uma pasta."
