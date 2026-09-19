import os
import json
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance,PointStruct, VectorParams
from sentence_transformers import SentenceTransformer



load_dotenv()

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

texts = []

for chunk in chunks:
    texts.append(chunk["text"])


embeddings = model.encode(texts)


# print(embeddings)
# print("Number of chunks",len(chunks))
# print("Vector size",len(embeddings[0]))
# print("First vector",embeddings[0])


client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    cloud_inference=True,
    timeout=60
)


if not client.collection_exists(collection_name="youtube_chunks"):
    client.create_collection(
        collection_name="youtube_chunks",
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )


points = []


for i in range(len(chunks)):
    point = PointStruct(
       id=i,
       vector=embeddings[i].tolist(),
       payload={
           "text": chunks[i]["text"],
            "start": chunks[i]["start"],
            "end": chunks[i]["end"]
       }
    )

    points.append(point)


batch_size = 20

for start in range(0, len(points), batch_size):

    batch = points[start:start + batch_size]

    client.upsert(
        collection_name="youtube_chunks",
        points=batch
    )

    print("Uploaded", len(batch), "points")

print("Stored", len(points), "chunks in Qdrant")