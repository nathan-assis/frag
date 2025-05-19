from fastapi import APIRouter

from . import messages

router = APIRouter()
router.include_router(messages.router, tags=["messages"])
