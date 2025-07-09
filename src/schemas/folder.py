from pathlib import Path

from pydantic import BaseModel, Field

from src.schemas.file import File


class Folder(BaseModel):
    path: Path = Field(..., description="Path of the folder to be indexed")
    data: list[File] = Field(
        default_factory=list, description="List of files contained in the folder"
    )
