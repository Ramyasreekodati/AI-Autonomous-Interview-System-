import random
from ai_modules.cv.face_mesh import FaceAnalyzer
from ai_modules.nlp.relevance_scorer import RelevanceScorer

analyzer = FaceAnalyzer()
scorer = RelevanceScorer()

def analyze_emotion(frame_bytes):
    analysis = analyzer.analyze_frame(frame_bytes)
    # Simple logic mapping: no face -> stressed (out of focus)
    if not analysis.get("face_detected", False):
        return "Not Focused"
    
    emotions = ["Neutral", "Happy", "Focused"]
    return random.choice(emotions)

def calculate_relevance(text):
    # This now uses a real transformer-based similarity
    # In a full app, we would compare text against expected model answers
    reference = "I understand the difference between supervised and unsupervised learning."
    relevance = scorer.calculate_relevance(text, reference)
    return relevance

def generate_session_summary(session_data):
    # This would generate the logic for the final scoring
    return {
        "overall_score": 85,
        "communication_skills": 90,
        "technical_knowledge": 80,
        "behavioral_score": 85,
        "final_recommendation": "HIRE"
    }
