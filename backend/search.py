from qdrant_client import QdrantClient
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


def search_notes(question):

    embedding_model = get_model()

    question_embedding = embedding_model.encode(question).tolist()

    results = client.query_points(
        collection_name="study_notes",
        query=question_embedding,
        limit=3
    )

    context = ""

    for point in results.points:
        context += point.payload["text"] + "\n\n"

    return context