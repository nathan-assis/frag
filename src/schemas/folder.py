from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class File(BaseModel):
    path: Path = Field(
        ...,
        description="Absolute file path",
        examples="/home/user/documents/file_name.txt",
    )
    file_name: str = Field(..., description="File name", examples="file_name.txt")
    extension: str = Field(
        ..., description="File extension", examples=[".pdf", ".txt", ".md"]
    )
    text: str = Field(..., description="File text")
    chunks: list[str] = Field(
        ..., description="List of text chunks extracted from the text"
    )
    embeddings: Any = Field(..., description="Vector representations of each chunk")


class Folder(BaseModel):
    path: Path = Field(..., description="Path of the folder to be indexed")
    data: list[File] = Field(
        default_factory=list, description="List of files contained in the folder"
    )
