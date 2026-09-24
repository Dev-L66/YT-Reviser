import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from groq import Groq


load_dotenv()

app = FastAPI()



# Qdrant
qdrant_client = QdrantClient(
    url= os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
     cloud_inference=True,
        timeout=60
)

# Embeddig model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Groq client

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

groq_model = "openai/gpt-oss-120b"


class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {
        "message": "Youtube Reviser API running."
    }

@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question

    question_embedding = embedding_model.encode(question)


    results = qdrant_client.query_points(
        collection_name = "youtube_chunks",
        query = question_embedding.tolist(),
        limit = 10
    )

    context = ""

    for result in results.points:
        context+=f"""
        Timestamp: {result.payload["start"]} - {result.payload["end"]}
        Text: {result.payload["text"]}
        """
    
    messages = [
        {
        "role": "system",
        "content": """Answer using only the provided video context.
                    If the context is insufficient, say so.
                    Do not invent information."""
        },
        {
            "role": "user",
            "content": f""" Video context: {context} 
                       Question: {question}"""
        }
    ]
    response = groq_client.chat.completions.create(model= groq_model, messages = messages)

    answer = response.choices[0].message.content

    return {
        "question": question,
        "answer": answer
    }



