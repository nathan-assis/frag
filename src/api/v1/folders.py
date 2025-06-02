from pathlib import Path

from fastapi import APIRouter, HTTPException

from src.schemas.folder import Folder, FolderOut

router = APIRouter()


@router.post("/folders", response_model=FolderOut)
def receive_folder(folder: Folder):
    path = validate_folder(folder.path)

    if not path.exists():
        raise HTTPException(status_code=400, detail="Caminho não encontrado.")

    if not path.is_dir():
        raise HTTPException(
            status_code=400, detail="O caminho informado não é uma pasta."
        )

    # feature: process files from folder
    # feature: store processed chunks in Milvus
    print(f"[INFO] Pasta registrada para uso: {path}")

    return FolderOut(
        status="success", message=f"Pasta '{path}' registrada com sucesso."
    )


def validate_folder(path_str: str) -> Path:
    path = Path(path_str)

    if not path.exists():
        raise HTTPException(status_code=400, detail="Caminho não encontrado.")

    if not path.is_dir():
        raise HTTPException(
            status_code=400, detail="O caminho informado não é uma pasta."
        )

    return path
