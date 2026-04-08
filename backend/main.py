from fastapi import FastAPI, WebSocket, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine, get_db
from database.models import models
from utils import auth
from utils.nlp_evaluator import nlp_evaluator
import datetime
import shutil
import os

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Interview System API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication Endpoints
@app.post("/auth/signup")
async def signup(email: str, password: str, full_name: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pass = auth.get_password_hash(password)
    new_user = models.User(email=email, hashed_password=hashed_pass, full_name=full_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}

@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Interview Endpoints (Phase 1.2)
@app.get("/questions")
async def get_questions(db: Session = Depends(get_db)):
    return db.query(models.Question).all()

@app.post("/interview/start")
async def start_interview(db: Session = Depends(get_db)):
    new_interview = models.Interview(user_id=1, status="active")
    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)
    return {"interview_id": new_interview.id, "status": "started"}

from utils.bias_reduction import bias_reducer

@app.post("/interview/submit")
async def submit_response(interview_id: int, question_id: int, answer: str, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # --- PHASE 5: BIAS REDUCTION ---
    purified_answer = bias_reducer.purify_answer(answer)
    
    # --- PHASE 3: CORE INTELLIGENCE ---
    
    # 1. Keyword Scoring (Foundation)
    kw_score = 0.0
    found_keywords = []
    if question.expected_keywords:
        answer_lower = purified_answer.lower()
        for kw in question.expected_keywords:
            if kw.lower() in answer_lower:
                kw_score += (1.0 / len(question.expected_keywords))
                found_keywords.append(kw)
    
    # 2. Semantic NLP Scoring (Step 3.1)
    semantic_score = 0.0
    if question.ideal_answer:
        semantic_score = nlp_evaluator.calculate_semantic_similarity(purified_answer, question.ideal_answer)
    
    # 3. Multi-Factor Fusion (Step 3.2)
    # Weights: 40% Keywords, 60% Semantic Depth
    # (Future-proof: This will eventually include Behavior and Emotion scores)
    final_score = (kw_score * 0.4) + (semantic_score * 0.6)
    
    # Scale to 10
    display_score = round(final_score * 10, 2)
    
    new_response = models.Response(
        interview_id=interview_id,
        question_id=question_id,
        answer_text=answer,
        score=display_score
    )
    db.add(new_response)
    db.commit()
    
    return {
        "status": "submitted", 
        "score": display_score, 
        "details": {
            "keywords_found": found_keywords,
            "semantic_similarity": round(semantic_score, 4)
        },
        "feedback": f"Your answer covered {len(found_keywords)} key topics and showed {round(semantic_score * 100)}% conceptual alignment."
    }



from utils.reporting import report_generator
from utils.transcription import transcriber

@app.post("/interview/end/{interview_id}")
async def end_interview(interview_id: int, db: Session = Depends(get_db)):
    interview = db.query(models.Interview).filter(models.Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    responses = db.query(models.Response).filter(models.Response.interview_id == interview_id).all()
    if not responses:
        return {"status": "completed", "final_score": 0.0, "message": "No responses found"}
    
    # 1. Answer Analysis
    avg_score = sum(r.score for r in responses) / len(responses)
    
    # 2. Behavior & Cheating Analysis (Step 3.3)
    alerts = active_alerts.get(interview_id, [])
    cheating_analysis = cheating_detector.analyze_session(alerts)
    
    # Calculate final score (weighted)
    behavior_score = 10.0 if not cheating_analysis["cheating_detected"] else (5.0 if cheating_analysis["risk_level"] == "Medium" else 2.0)
    final_weighted_score = (avg_score * 0.7) + (behavior_score * 0.3)
    
    interview.status = "completed"
    interview.end_time = datetime.datetime.utcnow()
    interview.total_score = final_weighted_score
    
    # Explainable Scoring (Step 3.4)
    breakdown = {
        "answer_quality": round(avg_score, 2),
        "behavior": behavior_score,
        "cheating_risk": cheating_analysis["risk_level"]
    }
    interview.score_breakdown = breakdown
    
    # Generate Reasoning Logs
    logs = []
    for r in responses:
        status_msg = "Excellent" if r.score > 8 else "Good" if r.score > 5 else "Needs Improvement"
        logs.append(f"Q{r.question_id}: {status_msg} (Score: {r.score})")
    
    if cheating_analysis["cheating_detected"]:
        logs.append(f"ALERT: Suspicious activity detected - {cheating_analysis['reason']}")
    
    interview.reasoning_logs = logs
    db.commit()
    
    # --- PHASE 5: REPORT GENERATION ---
    user = db.query(models.User).filter(models.User.id == interview.user_id).first()
    user_name = user.full_name if user else "Candidate"
    
    report_path = report_generator.generate_candidate_report(
        candidate_name=user_name,
        score_data={"total_score": round(final_weighted_score, 2), "breakdown": breakdown},
        feedback_logs=logs
    )
    
    # Clean up memory
    if interview_id in active_alerts:
        del active_alerts[interview_id]
    
    return {
        "status": "completed",
        "final_score": round(final_weighted_score, 2),
        "breakdown": breakdown,
        "report_url": report_path,
        "cheating_report": cheating_analysis
    }

# Endpoint for Audio Transcription (Phase 5.1)
@app.post("/interview/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    # Save temporary file
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    text = transcriber.transcribe(temp_path)
    os.remove(temp_path)
    
    return {"transcription": text}

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Interview System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

import base64
import cv2
import numpy as np
from utils.proctoring import proctoring_engine
from utils.cheating_detector import cheating_detector

# Session alert storage (In memory for simplicity, should be in DB for prod)
active_alerts = {}

# Placeholder for real-time signaling/alerts
@app.websocket("/ws/alerts/{interview_id}")
async def websocket_endpoint(websocket: WebSocket, interview_id: int):
    await websocket.accept()
    if interview_id not in active_alerts:
        active_alerts[interview_id] = []
        
    try:
        while True:
            # Receive base64 frame from frontend
            data = await websocket.receive_text()
            
            if data.startswith("data:image"):
                # Decode image
                encoded_data = data.split(',')[1]
                nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                # Analyze frame
                results = proctoring_engine.analyze_frame(frame)
                
                # Update session alerts
                if results["alerts"]:
                    for alert_type in results["alerts"]:
                        alert_body = {"type": alert_type, "timestamp": datetime.datetime.utcnow().isoformat()}
                        active_alerts[interview_id].append(alert_body)
                        
                        # Send alert back to frontend
                        await websocket.send_json({
                            "type": "ALERT",
                            "message": f"Suspicious activity: {alert_type}",
                            "alert_code": alert_type
                        })
                
                # Periodically send a summary or health check
                await websocket.send_json({"type": "HEARTBEAT", "status": "active"})
                
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()
