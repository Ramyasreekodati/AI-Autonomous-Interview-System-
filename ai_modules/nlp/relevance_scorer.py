from sentence_transformers import SentenceTransformer, util
import torch

class RelevanceScorer:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # Using a very lightweight model
        self.model = SentenceTransformer(model_name)
    
    def calculate_relevance(self, candidate_answer, reference_keywords):
        # Calculate cosine similarity between answer and expected keywords
        embeddings1 = self.model.encode(candidate_answer, convert_to_tensor=True)
        embeddings2 = self.model.encode(reference_keywords, convert_to_tensor=True)
        
        cosine_scores = util.cos_sim(embeddings1, embeddings2)
        return round(float(cosine_scores[0][0]), 2)

    def analyze_sentiment(self, text):
        # Placeholder for sentiment analysis (could use transformers pipeline)
        return "Positive" if "clear" in text.lower() or "understand" in text.lower() else "Neutral"
