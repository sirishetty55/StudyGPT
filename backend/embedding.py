from sentence_transformers import SentenceTransformer

model = None


def get_model():
    global model

    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


def generate_embeddings(chunks):

    embedding_model = get_model()

    embeddings = embedding_model.encode(chunks)

    return embeddings.tolist()