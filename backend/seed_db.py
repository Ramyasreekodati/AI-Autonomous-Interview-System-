from database.database import SessionLocal, engine
from database.models.models import Question, Base

def seed_questions():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Clear existing questions to ensure fresh seed with ideal_answers
    db.query(Question).delete()
    db.commit()

    questions = [
        {
            "text": "Explain the concept of Virtual DOM in React.",
            "category": "Technical",
            "difficulty": "Medium",
            "expected_keywords": ["virtual dom", "reconciliation", "diffing", "performance"],
            "ideal_answer": "The Virtual DOM is a lightweight copy of the real DOM. React uses it to keep track of changes in state. When a component updates, React creates a new virtual DOM tree and compares it with the previous one through a process called reconciliation or diffing, updating only the necessary parts of the real DOM for better performance."
        },
        {
            "text": "What is the difference between supervised and unsupervised learning?",
            "category": "AI/ML",
            "difficulty": "Easy",
            "expected_keywords": ["labeled", "labels", "clustering", "features"],
            "ideal_answer": "Supervised learning uses labeled datasets to train algorithms to classify data or predict outcomes. Unsupervised learning analyzes and clusters unlabeled datasets to discover hidden patterns or data groupings without human intervention."
        },
        {
            "text": "How do you handle conflict in a team environment?",
            "category": "Behavioral",
            "difficulty": "Easy",
            "expected_keywords": ["communication", "conflict resolution", "collaboration", "empathy"],
            "ideal_answer": "I handle conflict by first listening to all parties involved to understand different perspectives. I try to remain objective and focus on the problem rather than personalities. Through open communication and empathy, I work towards a collaborative solution that aligns with the team's goals."
        }
    ]

    for q in questions:
        db_q = Question(**q)
        db.add(db_q)
    
    db.commit()
    db.close()
    print("Questions seeded successfully!")

if __name__ == "__main__":
    seed_questions()
