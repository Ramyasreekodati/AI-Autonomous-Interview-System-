from fastapi import FastAPI, UploadFile, File, Form, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
import time
import json
import random
import os
import sys
from typing import List
from sqlalchemy.orm import Session

# Internal imports
from .database import engine, get_db, SessionLocal
from . import models
from app.services import ai_service

# Create tables
models.Base.metadata.create_all(bind=engine)

from fastapi.staticfiles import StaticFiles

app = FastAPI(title="AI Interview System")

# Serve reports as static files
os.makedirs("reports", exist_ok=True)
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

# Enabling CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Interview System Backend"}

@app.get("/questions")
def get_questions():
    questions_path = os.path.join(os.path.dirname(__file__), "questions.json")
    with open(questions_path, "r") as f:
        return json.load(f)

@app.post("/session/start")
def start_session(candidate_name: str = Form(...), db: Session = Depends(get_db)):
    session_id = f"sess_{int(time.time())}"
    db_session = models.CandidateSession(
        id=session_id,
        candidate_name=candidate_name,
        status="started"
    )
    db.add(db_session)
    db.commit()
    return {
        "candidate_name": candidate_name,
        "session_id": session_id,
        "status": "started",
        "timestamp": time.time()
    }

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
async def analyze_speech(
    session_id: str = Form(...), 
    question_id: int = Form(...),
    text: str = Form(...),
    db: Session = Depends(get_db)
):
    relevance_score = ai_service.calculate_relevance(text)
    
    # Save the answer
    db_answer = models.CandidateAnswer(
        session_id=session_id,
        question_id=question_id,
        answer_text=text,
        relevance_score=relevance_score,
        detailed_feedback={"sentiment": "Positive", "key_points": ["Technical communication"]}
    )
    db.add(db_answer)
    db.commit()

    return {
        "session_id": session_id,
        "status": "saved",
        "relevance_score": relevance_score
    }

@app.websocket("/ws/analyze/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    db = SessionLocal()
    try:
        while True:
            data = await websocket.receive_bytes()
            emotion = ai_service.analyze_emotion(data)
            
            if emotion == "Not Focused":
                alert = models.AlertLog(
                    session_id=session_id,
                    type="Focus",
                    message="Candidate lost focus or face not detected",
                    severity="Medium"
                )
                db.add(alert)
                db.commit()

            await websocket.send_json({
                "session_id": session_id,
                "emotion": emotion,
                "focus_score": 0.0 if emotion == "Not Focused" else 0.98,
                "alerts": ["Face not detected"] if emotion == "Not Focused" else []
            })
    except WebSocketDisconnect:
        print(f"Session {session_id} disconnected")
    finally:
        db.close()

from fpdf import FPDF

@app.get("/report/{session_id}")
def generate_report(session_id: str, db: Session = Depends(get_db)):
    session_data = db.query(models.CandidateSession).filter(models.CandidateSession.id == session_id).first()
    if not session_data:
        return {"error": "Session not found"}

    answers = db.query(models.CandidateAnswer).filter(models.CandidateAnswer.session_id == session_id).all()
    alerts = db.query(models.AlertLog).filter(models.AlertLog.session_id == session_id).all()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AI Interview Report", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Candidate Name: {session_data.candidate_name}", ln=True)
    pdf.cell(200, 10, txt=f"Session ID: {session_data.id}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {session_data.started_at.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Answer Summary", ln=True)
    pdf.set_font("Arial", size=10)
    for ans in answers:
        pdf.multi_cell(0, 10, txt=f"Q{ans.question_id}: {ans.answer_text[:100]}... [Score: {ans.relevance_score}]")
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Proctoring Alerts", ln=True)
    pdf.set_font("Arial", size=10)
    for alert in alerts:
        pdf.cell(200, 10, txt=f"- [{alert.severity}] {alert.type}: {alert.message}", ln=True)

    # Use a relative path for reports
    os.makedirs("reports", exist_ok=True)
    report_filename = f"report_{session_id}.pdf"
    report_path = os.path.join("reports", report_filename)
    pdf.output(report_path)
    
    session_data.final_report_url = f"/reports/{report_filename}"
    session_data.status = "completed"
    db.commit()

    return {"report_url": f"/reports/{report_filename}", "status": "completed"}

@app.get("/admin/sessions")
def get_sessions(db: Session = Depends(get_db)):
    return db.query(models.CandidateSession).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
