from qdrant_client import QdrantClient
from os import environ
from qdrant_client.models import Distance, VectorParams
from clients.qdrant import *
from qdrant_client.http.exceptions import UnexpectedResponse
from json import loads
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
from qdrant_client import models
import uuid
from contextlib import contextmanager

class qdrant_internal:
    def __init__(self):
        self.client = self.get_client()

    # @contextmanager
    def get_client(self):
        client = QdrantClient(url=environ.get('QDRANT_URL'))
        return client
        # try:
        #     yield client
        # finally:
        #     client.close()
        #     print("Qdrant client connection closed.")

    def get_or_create_collection(self, collection_name=None, vectors_config=None, existance_check=True, force_recreate = False):
        """
        Create collection on qdrant db
        """
        collection_name="test_collection" if collection_name is None else collection_name
        results = None

        try:
            if not force_recreate:
                try:
                    if existance_check:
                        results = self.client.get_collection(collection_name=collection_name)
                        print(f"Checking for existing collection {results}")
                        if results.status.value=='green':
                            print(f"Pre-existed collection {collection_name}")
                            return True
                except:
                    pass
                finally:
                    results = self.client.create_collection(
                        collection_name=collection_name,
                        vectors_config=VectorParams(size=4, distance=Distance.DOT) if vectors_config is None else vectors_config,
                    )
                    if self.client.collection_exists(collection_name):
                        print("Collection created successfully!")
                        print(f"got job response: {results}")
                        results = True
                    else:
                        results = False
        except UnexpectedResponse as e:
            if e.status_code == 409:
                print(f"Error --- {e.reason_phrase} :: {loads(e.content)['status']['error']}")

        except Exception as e:
            print(f"got an exception: {e}")
        return results
    
    def update_optimizer_configs(self, COLLECTION_NAME):
        # configuration optimizes Qdrant for bulk vector ingestion
        self.client.update_collection(
            collection_name=COLLECTION_NAME,
            optimizers_config=models.OptimizersConfigDiff(
                indexing_threshold=20000
            )
        )
    
    def update_quantization_configs(self, COLLECTION_NAME):
        # Compresses vectors for reduced memory usage and faster searches
        self.client.update_collection(
            collection_name=COLLECTION_NAME,
            quantization_config=models.ScalarQuantization(
                scalar=models.ScalarQuantizationConfig(
                    type=models.ScalarType.INT8,
                    quantile=0.99,
                    always_ram=True
                )
            )
        )

    def prepare_point_struct(self, vectors: list, columns_title: list, payloads:list) -> list:
        """
        Make points
        """
        points: list = []
        for vector, payload in zip(vectors, payloads):
            unique_id = str(uuid.uuid4())

            print(f"type of pay: {type(payload), payload}")
            points.append(
                PointStruct(
                    id=unique_id,
                    vector=vector,
                    payload=payload
                )
            )
        return points


    def add_point_structure(self, collection_name=None, points=None):
        """
        Add points on vectors, with details to db
        """
        test_points = [
                PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
                PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London"}),
                PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow"}),
                PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York"}),
                PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing"}),
                PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai"}),
            ]
        default_collection = 'test_collection'

        if points and collection_name:
            operation_info = self.client.upsert(
                collection_name=collection_name,
                wait=True,
                points=points
            )

        print(operation_info)

        return operation_info

    # def add_batch_points(self, collection_name, payloads, vectors):
    #     operation_info = self.client.upsert(
    #         collection_name=collection_name,
    #         wait=True,
    #         points=models.Batch(
    #             ids: list = [],
    #             payloads=[
    #                 {"color": "red"},
    #             ],
    #             vectors = [
    #                 []
    #             ]
    #         ),
    #     )

    def search_query(self, collection_name=None, query=None, with_payload=False, limit=None):
        """
        """
        search_result = self.client.query_points(
            collection_name="test_collection" if collection_name is None else collection_name,
            query=[0.2, 0.1, 0.9, 0.7] if query is None else query,
            with_payload=False if with_payload is None else with_payload,
            limit=3 if limit is None else limit
        ).points

        return search_result

    def search_query_filter(self,):
        search_result = self.client.query_points(
            collection_name="test_collection",
            query=[0.2, 0.1, 0.9, 0.7],
            query_filter=Filter(
                must=[FieldCondition(key="city", match=MatchValue(value="London"))]
            ),
            with_payload=True,
            limit=3,
        ).points

        return search_result
