from fastapi import APIRouter

from src.schemas.message import Message

router = APIRouter()


@router.post("/messages", response_model=Message)
def send_message(message: Message):
    # response = process_message(message.text)

    return Message(text="# TODO: implement rag!!!")
