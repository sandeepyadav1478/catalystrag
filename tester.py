from clients.qdrant import qdrant_internal
from props.csv_importer import upload_data
from props.get_embedding_func import converter_to_embed
from qdrant_client.http.models import VectorParams, Distance

collection_name = 'kaggle_finance'

# import file
data = upload_data()

# get embedded data
columns_title, data, vectors = converter_to_embed(data)

print(f"payload type: {type(columns_title)}, vectors type: {type(vectors)}")
# prep. client
qc = qdrant_internal()

## prep. vector configs
# for text, consine distance is recommended
distance_metric = Distance.COSINE
# vector size will depend upon number of columns
vector_size = len(vectors)
vector_configs = VectorParams(
    size=vector_size,
    distance=distance_metric
)

# create collection on qdrant db
ops = qc.get_or_create_collection(
    collection_name=collection_name,
    vectors_config=vector_configs
)
print(f"Collection creation task status: {ops}")

# create points on collection
if ops == True:
    print(f"Preparing points")
    points = qc.prepare_point_struct(vectors, columns_title, data)
    print(f"Adding to db")
    op_result = qc.add_point_structure(collection_name=collection_name, points=points)
    print(f"Insertion job is done {op_result}")


# client = qdrant_internal()
# client.add_point_structure()
# client.search_query()
# print(client.search_query_filter())