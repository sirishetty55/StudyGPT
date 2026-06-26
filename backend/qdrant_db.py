from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(
    host="qdrant",
    port=6333
)

collections = client.get_collections()

collection_names = [
    collection.name
    for collection in collections.collections
]

if "study_notes" not in collection_names:

    client.create_collection(
        collection_name="study_notes",
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

print("Connected to Qdrant!")
print("Collection Ready!")