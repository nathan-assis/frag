from pydantic import BaseModel, Field


class Folder(BaseModel):
    path: str = Field(..., description="Caminho da pasta a ser indexada")
    files: list[str] = Field(
        default_factory=list, description="Lista de arquivos da pasta"
    )
