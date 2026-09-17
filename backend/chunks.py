import json

with open("transcripts/transcript.json","r", encoding="utf-8") as f:
    transcript = json.load(f)



chunks = []
current_text = []
chunk_start = None
chunk_end = None


for segment in transcript:
    if chunk_start is None:
        chunk_start = segment["start"]


    current_text.append(segment["text"])
    chunk_end = segment["end"]

    if chunk_start + chunk_end >=30:
        chunks.append({
            "start": chunk_start,
            "end": chunk_end,
            "text": "".join(current_text)
        })


    current_text = []
    chunk_start = None
    chunk_end = None


if current_text:
    chunks.append({
        "start": chunk_start,
        "end": chunk_end,
        "text":"".join(current_text)
    })


with open("chunks.json", "w", encoding = "utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2 )


print(f"Created {len(chunks)} chunks")

