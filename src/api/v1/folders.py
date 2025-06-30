from fastapi import APIRouter

from src.schemas.folder import Folder
from src.schemas.response import Response
from src.services.rag_pipeline import RAGPipeline

router = APIRouter()


@router.post("/folders", response_model=Response)
def receive_folder(folder: Folder):
    RAGPipeline.process_folder(folder.path)
    print(f"[INFO] Pasta registrada para uso: {folder.path}")

    return Response(
        status="success", message=f"Pasta '{folder.path}' registrada com sucesso."
    )
