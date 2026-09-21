import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()


client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    cloud_inference=True,
    timeout=60
)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


question = input("Ask a question about the video: ")

question_embedding = model.encode(question)

results = client.query_points(
    collection_name = "youtube_chunks",
    query= question_embedding.tolist(),
    limit=5
)

context = ""

for result in results.points:
    context += result.payload["text"] + "\n"
    # print("Result")
    # print("Score:", result.score)
    # print("Text:", result.payload["text"])
    # print("Start:", result.payload["start"])
    # print("End:", result.payload["end"])


groq_client = Groq(api_key= os.getenv("GROQ_API_KEY"))

groq_model = "openai/gpt-oss-120b"

messages = [
    {
      "role": "system",
      "content": "Answer the user's question using only the provided video context."
    },

    {
      "role": "user",
      "content": f""" Video context: {context} Question: {question}"""
    }
]

response = groq_client.chat.completions.create(
    model= groq_model, messages=messages
)


answer = response.choices[0].message.content

print("\nAnswer:")

print(answer)

