from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pymupdf
from fastapi import HTTPException

from src.schemas.folder import Folder

from . import chunking, embedding


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

    def __get_file_content(file: Path) -> str:
        try:
            suffix = file.suffix.lower()
            match suffix:
                case ".txt" | ".md":
                    return file.read_text(encoding="utf-8")
                case ".pdf":
                    with pymupdf.open(file) as doc:
                        text = chr(12).join([page.get_text() for page in doc])
                    return text
        except Exception as e:
            print(f"[WARN] Erro ao ler {file}: {e}")
            return None

    def __process_content(content: str) -> list[tuple[str, list[float]]]:
        chunks = chunking.fixed_size_with_overlap(content)
        vectors = embedding.generate_embedding(chunks)

        return list(zip(chunks, vectors, strict=False))

    @staticmethod
    def process_folder(path: str) -> None:
        RAGPipeline.__set_folder(path)

        folder_data = []
        with ThreadPoolExecutor() as executor:
            content_future = {
                executor.submit(RAGPipeline.__get_file_content, f): f
                for f in RAGPipeline.__folder.files
            }

            file_futures = []
            for future in as_completed(content_future):
                content = future.result()
                if content is None:
                    continue

                file_future = executor.submit(RAGPipeline.__process_content, content)
                file_futures.append(file_future)

            for future in as_completed(file_futures):
                result = future.result()
                if result is not None:
                    folder_data.extend(result)
