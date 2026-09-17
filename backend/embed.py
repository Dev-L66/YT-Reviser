import json
from sentence_transformers import SentenceTransformer


with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

texts = []

for chunk in chunks:
    texts.append(chunk["text"])


embeddings = model.encode(texts)


# print(embeddings)
print("Number of chunks",len(chunks))
print("Vector size",len(embeddings[0]))
print("First vector",embeddings[0])