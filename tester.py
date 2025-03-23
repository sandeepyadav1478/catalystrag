from clients.qdrant import qdrant_internal

client = qdrant_internal()
client.add_point_structure()
client.search_query()
print(client.search_query_filter())