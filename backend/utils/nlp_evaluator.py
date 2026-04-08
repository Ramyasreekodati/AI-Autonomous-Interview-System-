import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NLPEvaluator:
    """
    Advanced NLP Evaluator for Phase 3.
    Uses Transformer-based semantic similarity to compare answers.
    """
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        logger.info(f"Initializing NLP Evaluator with model: {model_name}")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            self.enabled = True
        except Exception as e:
            logger.error(f"Failed to load transformer model: {e}")
            self.enabled = False

    def _mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def _get_embedding(self, text):
        encoded_input = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt', max_length=512)
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        return self._mean_pooling(model_output, encoded_input['attention_mask'])

    def calculate_semantic_similarity(self, candidate_answer, ideal_answer):
        """
        Calculates cosine similarity between two text strings.
        Returns a score between 0.0 and 1.0.
        """
        if not self.enabled or not candidate_answer or not ideal_answer:
            return self._fallback_similarity(candidate_answer, ideal_answer)
        
        try:
            emb1 = self._get_embedding(candidate_answer)
            emb2 = self._get_embedding(ideal_answer)
            
            cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
            similarity = cos(emb1, emb2)
            # Normalize score (cosine similarity can be negative, but usually > 0 for text)
            score = max(0.0, float(similarity.item()))
            return score
        except Exception as e:
            logger.warning(f"Error during semantic similarity calculation: {e}")
            return self._fallback_similarity(candidate_answer, ideal_answer)

    def _fallback_similarity(self, text1, text2):
        """
        Simple keyword-based fallback if transformer model is unavailable.
        """
        if not text1 or not text2:
            return 0.0
        
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0

# Singleton instance
nlp_evaluator = NLPEvaluator()
