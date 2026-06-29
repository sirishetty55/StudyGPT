from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
    MatchAny
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

        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return model


def search_notes(question, filenames=None):

    embedding_model = get_model()

    question_embedding = embedding_model.encode(
        question
    ).tolist()

    search_filter = None

    if filenames and len(filenames) > 0:

        search_filter = Filter(

            must=[

                FieldCondition(

                    key="filename",

                    match=MatchAny(
                        any=filenames
                    )

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

    sources = set()

    for point in results.points:

        context += point.payload["text"] + "\n\n"

        sources.add(
            point.payload["filename"]
        )

    return context, list(sources)