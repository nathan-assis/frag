from pathlib import Path

import pymupdf

from src.schemas.file import File as FileSchema
from src.services.chunking import fixed_size_with_overlap
from src.services.embedding import generate_embedding


class File:
    def __init__(self, path: Path):
        self.__path = path if path.exists() and path.is_file() else None
        self.__file_name = str(self.__path).split("/")[-1] if self.__path else None
        self.__extension = self.__path.suffix.lower() if self.__path else None
        self.__text = self.__get_text()
        self.__chunks = fixed_size_with_overlap(self.__text)
        self.__embeddings = generate_embedding(self.__chunks)

    def __get_text(self) -> str:
        text = None

        match self.__extension:
            case ".pdf":
                with pymupdf.open(self.__path) as doc:
                    text = chr(12).join([page.get_text() for page in doc])
            case ".txt" | ".md":
                text = self.__path.read_text(encoding="utf-8")

        return text

    def get_file(self) -> dict[FileSchema]:
        return {
            "path": self.__path,
            "file_name": self.__file_name,
            "extension": self.__extension,
            "text": self.__text,
            "chunks": self.__chunks,
            "embeddings": self.__embeddings,
        }
