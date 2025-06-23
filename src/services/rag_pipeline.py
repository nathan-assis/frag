from pathlib import Path

from fastapi import HTTPException

from src.schemas.folder import Folder


class RAGPipeline:
    __folder: Folder = None

    def __set_folder(path_str: str) -> None:
        def set_path() -> None:
            path = Path(path_str)

            if not (path.exists() and path.is_dir()):
                raise HTTPException(status_code=400, detail="Invalid path")

            RAGPipeline.__folder.path = path

        def set_files() -> None:
            files = list(RAGPipeline.__folder.path.rglob("*"))
            RAGPipeline.__folder.files = [f for f in files if f.is_file()]

        if RAGPipeline.__folder is None:
            RAGPipeline.__folder = Folder(path="", files=[])

        set_path()
        set_files()

    @staticmethod
    def process_folder(path: str) -> None:
        RAGPipeline.__set_folder(path)
