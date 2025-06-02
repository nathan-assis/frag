from pydantic import BaseModel, Field


class Folder(BaseModel):
    path: str = Field(..., description="Caminho da pasta a ser indexada")


class FolderOut(BaseModel):
    status: str
    message: str
