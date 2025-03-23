from qdrant_client import QdrantClient
from os import environ
from qdrant_client.models import Distance, VectorParams
from clients.qdrant import *
from qdrant_client.http.exceptions import UnexpectedResponse
from json import loads
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue

class qdrant_internal:
    def __init__(self):
        self.client = self.get_client()


    def get_client(self):
        return QdrantClient(url=environ.get('QDRANT_URL'))
    

    def add_collection(self, collection_name=None, vectors_config=None):
        """
        Create collection on qdrant db
        """

        try:
            results = self.client.create_collection(
                collection_name="test_collection" if collection_name is None else collection_name,
                vectors_config=VectorParams(size=4, distance=Distance.DOT) if vectors_config is None else vectors_config,
            )
            print(f"got job response: {results.__dict__}")
        except UnexpectedResponse as e:
            if e.status_code == 409:
                print(f"Error --- {e.reason_phrase} :: {loads(e.content)['status']['error']}")

        except Exception as e:
            print(f"got an exception: {type(e)}")
        return results

    def add_point_structure(self, collection_name=None, points=None):
        """
        Add dots on vectors, with details
        """

        operation_info = self.client.upsert(
            collection_name="test_collection" if collection_name is None else collection_name,
            wait=True,
            points=[
                PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
                PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London"}),
                PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow"}),
                PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York"}),
                PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing"}),
                PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai"}),
            ] if points is None else points,
        )

        print(operation_info)

        return operation_info

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
