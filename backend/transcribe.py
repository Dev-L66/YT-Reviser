import whisper
import json

model = whisper.load_model("base")
result = model.transcribe("audio/Data Engineer Roadmap： Built From 22,000 Real Job Ads.m4a")


transcript = []


for segment in result["segments"]:
    transcript.append({
     "start": segment["start"],
     "end": segment["end"],
     "text":segment["text"]
    })

with open("transcripts/transcript.json", "w", encoding="utf-8") as f:
    json.dump(transcript, f, ensure_ascii=False, indent=2)

print("Transcript saved!")
    
