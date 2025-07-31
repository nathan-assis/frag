from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from src.database.repository import Repository
from src.models.generate_answer import generate_answer
from src.services.embedding import generate_embedding
from src.services.file import File


class RAGPipeline:
    __folder: Path = None

    @staticmethod
    def process_message(message: str) -> str:
        message_embedding = generate_embedding(message)
        data = None
        if RAGPipeline.__folder is not None:
            db = Repository()
            data = db.search(message_embedding.tolist())
        return generate_answer(message, data)

    @staticmethod
    def process_folder(path_str: str) -> None:
        RAGPipeline.__folder = Path(path_str)
        files = [
            file for file in list(RAGPipeline.__folder.rglob("*")) if file.is_file()
        ]

        data = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(File, file) for file in files]

            for future in as_completed(futures):
                data.extend(future.result().get_file())

        db = Repository()
        db.upsert(data)
