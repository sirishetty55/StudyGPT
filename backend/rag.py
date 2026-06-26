from ollama import Client
from search import search_notes

client = Client(
    host="http://host.docker.internal:11434"
)


def ask_rag(question):

    context = search_notes(question)

    prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]