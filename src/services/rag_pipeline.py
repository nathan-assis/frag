from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from src.database.repository import Repository
from src.services.file import File


class RAGPipeline:
    @staticmethod
    def process_folder(path_str: str) -> None:
        files = [file for file in list(Path(path_str).rglob("*")) if file.is_file()]

        data = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(File, file) for file in files]

            for future in as_completed(futures):
                data.append(future.result().get_file())

        db = Repository()
        db.upsert(data)
