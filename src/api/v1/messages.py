from fastapi import APIRouter

from src.schemas.message import Message
from src.schemas.response import Response

router = APIRouter()


@router.post("/messages", response_model=Response)
def send_message(message: Message):
    # response = process_message(message.text)

    return Response(status="success", message="# TODO: implement rag!!!")
