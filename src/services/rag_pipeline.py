from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from src.schemas.folder import Folder as FolderSchema
from src.services.file import File


class RAGPipeline:
    __folder: FolderSchema = None

    @staticmethod
    def process_folder(path_str: str) -> None:
        if RAGPipeline.__folder is None:
            RAGPipeline.__folder = FolderSchema(path=Path(path_str), data=[])

        files = [
            file
            for file in list(RAGPipeline.__folder.path.rglob("*"))
            if file.is_file()
        ]

        RAGPipeline.__folder.data = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(File, file) for file in files]

            for future in as_completed(futures):
                RAGPipeline.__folder.data.append(future.result().get_file())

        # TODO: save to milvus
