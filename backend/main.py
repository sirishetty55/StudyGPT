from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from database import engine, SessionLocal
from models import Base, User
from schemas import UserCreate
from schemas_chat import ChatRequest

from pdf_utils import extract_text
from chunking import create_chunks
from embedding import generate_embeddings
from qdrant_store import store_embeddings
from rag import ask_rag

from qdrant_client import QdrantClient

import shutil
import qdrant_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

client = QdrantClient(
    host="qdrant",
    port=6333
)


@app.get("/")
def home():

    return {
        "message": "StudyGPT Backend Running"
    }


@app.post("/users")
def create_user(user: UserCreate):

    db = SessionLocal()

    new_user = User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }


@app.get("/users")
def get_users():

    db = SessionLocal()

    return db.query(User).all()


@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):

    points = client.scroll(
        collection_name="study_notes",
        limit=10000,
        with_payload=True
    )[0]

    uploaded_files = {
        point.payload["filename"]
        for point in points
    }

    if file.filename in uploaded_files:

        return {
            "success": False,
            "message": f"{file.filename} already exists."
        }

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)

    if len(text.strip()) == 0:

        return {
            "success": False,
            "message": "No readable text found in the PDF."
        }

    chunks = create_chunks(text)

    embeddings = generate_embeddings(chunks)

    store_embeddings(
        chunks,
        embeddings,
        file.filename
    )

    return {

        "success": True,

        "filename": file.filename,

        "stored_in_qdrant": True

    }


@app.get("/files")
def list_files():

    points = client.scroll(
        collection_name="study_notes",
        limit=10000,
        with_payload=True
    )[0]

    files = sorted({

        point.payload["filename"]

        for point in points

    })

    return {

        "total_files": len(files),

        "files": files

    }


@app.delete("/files/{filename}")
def delete_file(filename: str):

    points = client.scroll(
        collection_name="study_notes",
        limit=10000,
        with_payload=True
    )[0]

    ids = []

    for point in points:

        if point.payload["filename"] == filename:

            ids.append(point.id)

    if len(ids) == 0:

        return {

            "success": False,

            "message": "File not found."

        }

    client.delete(

        collection_name="study_notes",

        points_selector=ids

    )

    return {

        "success": True,

        "message": f"{filename} deleted successfully."

    }
@app.post("/ask")
def ask(chat: ChatRequest):

    result = ask_rag(

        question=chat.question,

        filenames=chat.filenames

    )

    return {

        "question": chat.question,

        "answer": result["answer"],

        "sources": result["sources"]

    }