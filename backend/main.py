from fastapi import FastAPI, UploadFile, File
from database import engine, SessionLocal
from models import Base, User
from schemas import UserCreate
from pdf_utils import extract_text
from chunking import create_chunks
from embedding import generate_embeddings
from qdrant_store import store_embeddings
from rag import ask_rag
import shutil

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "StudyGPT Backend Running"}


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

    users = db.query(User).all()

    return users


@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)

    chunks = create_chunks(text)

    embeddings = generate_embeddings(chunks)

    store_embeddings(chunks, embeddings)

    return {
        "filename": file.filename,
        "text_length": len(text),
        "number_of_chunks": len(chunks),
        "embedding_dimension": len(embeddings[0]),
        "stored_in_qdrant": True
    }


@app.get("/ask")
def ask(question: str):

    answer = ask_rag(question)

    return {
        "question": question,
        "answer": answer
    }