from fastapi import APIRouter

from . import folders, messages

router = APIRouter()
router.include_router(messages.router, tags=["messages"])
router.include_router(folders.router, tags=["folders"])
