import random
from ai_modules.cv.face_mesh import FaceAnalyzer

analyzer = FaceAnalyzer()

def analyze_emotion(frame_bytes):
    analysis = analyzer.analyze_frame(frame_bytes)
    # Simple logic mapping: no face -> stressed (out of focus)
    if not analysis.get("face_detected", False):
        return "Not Focused"
    
    emotions = ["Neutral", "Happy", "Focused"]
    return random.choice(emotions)

def calculate_relevance(text):
    # This would use a transformer model
    return round(random.uniform(0.7, 1.0), 2)

def generate_session_summary(session_data):
    # This would generate the logic for the final scoring
    return {
        "overall_score": 85,
        "communication_skills": 90,
        "technical_knowledge": 80,
        "behavioral_score": 85,
        "final_recommendation": "HIRE"
    }
