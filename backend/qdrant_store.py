from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid

client = QdrantClient(
    host="qdrant",
    port=6333
)


def store_embeddings(chunks, embeddings, filename):

    points = []

    for chunk, embedding in zip(chunks, embeddings):

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "filename": filename
                }
            )
        )

    client.upsert(
        collection_name="study_notes",
        points=points,
        wait=True
    )