from pathlib import Path

from fastapi import HTTPException


class RAGPipeline:
    __folder_path: Path = None

    def __validate_folder(folder: str) -> Path:
        folder_path = Path(folder)

        if folder_path.exists() and folder_path.is_dir():
            return folder_path

        raise HTTPException(status_code=400, detail="Caminho inválido")

    def __process_folder() -> None:
        pass

    @staticmethod
    def process_folder(folder: str) -> None:
        RAGPipeline.__folder_path = RAGPipeline.__validate_folder(folder)
        RAGPipeline.__process_folder()

    @staticmethod
    def process_message() -> None:
        pass
