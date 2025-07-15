from fastapi import APIRouter

from src.schemas.message import Message
from src.schemas.response import Response
from src.services.rag_pipeline import RAGPipeline

router = APIRouter()


@router.post("/messages", response_model=Response)
def send_message(message: Message):
    response = RAGPipeline.process_message(message.text)

    return Response(
        status="success",
        message="",
        data=response,
    )
