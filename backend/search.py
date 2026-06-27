from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue
)
from sentence_transformers import SentenceTransformer

client = QdrantClient(
    host="qdrant",
    port=6333
)

model = None


def get_model():
    global model

    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


def search_notes(question, filename=None):

    embedding_model = get_model()

    question_embedding = embedding_model.encode(question).tolist()

    search_filter = None

    if filename:

        search_filter = Filter(
            must=[
                FieldCondition(
                    key="filename",
                    match=MatchValue(value=filename)
                )
            ]
        )

    results = client.query_points(
        collection_name="study_notes",
        query=question_embedding,
        query_filter=search_filter,
        limit=5
    )

    context = ""

    sources = list(dict.fromkeys(sources))

    for point in results.points:

        context += point.payload["text"] + "\n\n"

        sources.add(point.payload["filename"])

    return context, list(sources)