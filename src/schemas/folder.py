from pathlib import Path

from pydantic import BaseModel, Field


class Folder(BaseModel):
    path: Path = Field(..., description="Caminho da pasta a ser indexada")
    files: list[Path] = Field(
        default_factory=list, description="Lista de arquivos da pasta"
    )
