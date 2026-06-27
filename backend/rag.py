from search import search_notes
from ollama import Client

client = Client(host="http://host.docker.internal:11434")


def ask_rag(question, filename=None):

    context, sources = search_notes(question, filename)

    if context.strip() == "":
        return {
            "answer": "I couldn't find that information in the uploaded notes.",
            "sources": []
        }

    prompt = f"""
You are StudyGPT.

Answer ONLY using the study notes below.

Rules:

- Never invent information.
- If answer isn't present, say:
"I couldn't find that information in the uploaded notes."

- Reply in clean markdown.

- Use bullet points whenever possible.

- If steps are asked,
return numbered steps.

- Do NOT mention "according to context".

- At the end NEVER write:
"According to study notes"

Only answer naturally.

Study Notes:

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

    return {
        "answer": response["message"]["content"],
        "sources": sources
    }