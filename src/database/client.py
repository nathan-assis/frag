from pymilvus import DataType, MilvusClient

import src.database.consts as Constants


class Client:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance._client = MilvusClient(Constants.DATABASE)
            cls.__instance._create_collection()
        return cls.__instance

    @property
    def client(self) -> MilvusClient:
        return self._client

    def _create_collection(self):
        if not self._client.has_collection(Constants.COLLECTION):
            self._client.create_collection(
                collection_name=Constants.COLLECTION,
                schema=self._create_schema(),
                index_params=self._create_index_params(),
                dimension=Constants.DIMENSION,
            )

        self._client.load_collection(Constants.COLLECTION)

    def _create_schema(self):
        schema = self._client.create_schema()

        schema.add_field(
            field_name="path",
            is_primary=True,
            datatype=DataType.VARCHAR,
            nullable=False,
            max_length=1024,
        )
        schema.add_field(
            field_name="file_name",
            datatype=DataType.VARCHAR,
            nullable=False,
            max_length=100,
        )
        schema.add_field(
            field_name="extension",
            datatype=DataType.VARCHAR,
            nullable=False,
            max_length=6,
        )
        schema.add_field(
            field_name="text", datatype=DataType.VARCHAR, nullable=True, max_length=4096
        )
        schema.add_field(
            field_name="chunks",
            datatype=DataType.VARCHAR,
            nullable=True,
            max_length=4096,
        )
        schema.add_field(
            field_name="embeddings",
            datatype=DataType.FLOAT_VECTOR,
            dim=Constants.DIMENSION,
        )

        return schema

    def _create_index_params(self):
        index_params = self._client.prepare_index_params()

        index_params.add_index(
            field_name="embeddings",
            index_type="IVF_SQ8",
            metric_type="COSINE",
            params={"nlist": 128},
            index_name="embeddings_ivf_sq8_cosine",
        )

        return index_params
