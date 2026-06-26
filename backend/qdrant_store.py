from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

client = QdrantClient(
    host="qdrant",
    port=6333
)


def store_embeddings(chunks, embeddings):

    points = []

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        points.append(
            PointStruct(
                id=i,
                vector=embedding,
                payload={"text": chunk}
            )
        )

    client.upsert(
        collection_name="study_notes",
        points=points
    )