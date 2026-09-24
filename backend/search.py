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
    limit=10
)

context = ""

for result in results.points:
    # print({result.payload["start"]} - {result.payload["end"]})
    context += f"""
    Timestamp: {result.payload["start"]} - {result.payload["end"]}
    Text: {result.payload["text"]}"""
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
      "content": "If the context does not contain enough information to answer the question, say so. Do not make up information."
    },

    {
      "role": "user",
      "content": f""" Video context: {context} Question: {question}"""
    }
]

response = groq_client.chat.completions.create(
    model= groq_model, messages=messages, stream=True
)


for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)


for result in results.points[:3]:
    start = int(result.payload["start"])

    minutes = start//60
    seconds = start % 60

    youtube_url = (
       f"https://www.youtube.com/watch?v=kIk8tj0rbo0&t={start}" 
    )

    print(f"{minutes}:{seconds:02d} - {youtube_url}")
