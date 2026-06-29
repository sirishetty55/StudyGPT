from search import search_notes
from ollama import Client

client = Client(
    host="http://host.docker.internal:11434"
)


def ask_rag(question, filenames=None):

    q = question.lower().strip()

    # ---------- Greetings ----------

    if q in [
        "hi",
        "hello",
        "hey",
        "hii",
        "heyy"
    ]:

        return {
            "answer":
"""# 👋 Hello!

I'm **StudyGPT**.

Upload one or more PDFs and I'll answer questions **only from your study notes**.

Happy studying! 📚✨
""",
            "sources":[]
        }

    # ---------- Thanks ----------

    if q in [
        "thanks",
        "thank you",
        "thankyou",
        "ty"
    ]:

        return {

            "answer":
"""😊 You're welcome!

I'm always here if you need help with your notes.

Good luck with your studies! 🚀
""",

            "sources":[]

        }

    # ---------- Identity ----------

    if q in [

        "who are you",

        "what are you"

    ]:

        return {

            "answer":
"""🤖 I'm **StudyGPT**.

I can:

- 📄 Read your PDFs
- 🔍 Search using AI
- 🧠 Answer using only your uploaded notes
- 📚 Search multiple PDFs together

Ask me anything from your study material!
""",

            "sources":[]

        }

    # ---------- How are you ----------

    if q == "how are you":

        return {

            "answer":
"""😄 I'm doing great!

Ready to help you study.

Ask me anything from your uploaded PDFs! 📚
""",

            "sources":[]

        }

    # ---------- Semantic Search ----------

    context, sources = search_notes(
        question,
        filenames
    )

    if context.strip() == "":

        return {

            "answer":
"""🔍 I couldn't find that information in the selected PDFs.

Try:

- selecting another PDF
- asking differently
- uploading notes containing this topic
""",

            "sources":[]

        }

    prompt = f"""
You are StudyGPT.

Rules:

- Answer ONLY using the provided notes.
- Never invent information.
- Reply in beautiful markdown.
- Use headings.
- Use bullet points.
- Use numbered steps if needed.
- Explain simply.
- Never mention "context" or "study notes".

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

                "role":"user",

                "content":prompt

            }

        ]

    )

    return {

        "answer":response["message"]["content"],

        "sources":sources

    }