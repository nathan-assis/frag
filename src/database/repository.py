import src.database.consts as Constants
from src.database.client import Client
from src.schemas.file import File as FileSchema


class Repository:
    def __init__(self):
        self._client = Client().client

    def upsert(self, data: list[FileSchema]) -> None:
        self._client.upsert(collection_name=Constants.COLLECTION, data=data)

    def search(self, query_vector: list[float], top_k: int = 5) -> list[dict]:
        results = self._client.search(
            collection_name=Constants.COLLECTION,
            data=[query_vector],
            limit=top_k,
            output_fields=["path", "file_name", "text", "chunks"],
            search_params={"metric_type": "COSINE", "params": {"nprobe": 10}},
        )

        return results[0]
