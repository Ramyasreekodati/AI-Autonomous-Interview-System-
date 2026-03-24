from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import time
import json
import random
from typing import List
from app.services import ai_service

app = FastAPI(title="AI Interview System")

# Enabling CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import json

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Interview System Backend"}

@app.get("/questions")
def get_questions():
    with open("c:/Users/Lenovo/Desktop/AI interview/ai-interview-system/backend/app/questions.json", "r") as f:
        return json.load(f)

@app.post("/session/start")
def start_session(candidate_name: str = Form(...)):
    session_id = f"sess_{int(time.time())}"
    return {
        "candidate_name": candidate_name,
        "session_id": session_id,
        "status": "started",
        "timestamp": time.time()
    }

from app.services import ai_service

@app.post("/analyze/frame")
async def analyze_frame(session_id: str = Form(...), file: UploadFile = File(...)):
    emotion = ai_service.analyze_emotion(await file.read())
    return {
        "session_id": session_id,
        "emotion": emotion,
        "focus_score": round(random.uniform(0.8, 1.0), 2),
        "anomalies": []
    }

@app.post("/analyze/speech")
async def analyze_speech(session_id: str = Form(...), text: str = Form(...)):
    relevance_score = ai_service.calculate_relevance(text)
    return {
        "session_id": session_id,
        "sentiment": "Positive",
        "relevance_score": relevance_score,
        "key_points": ["Strong technical communication", "Clear articulation"]
    }

@app.get("/report/{session_id}")
def generate_report(session_id: str):
    # Placeholder for PDF report generation
    return {"report_url": f"/reports/report_{session_id}.pdf"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
