import re

class BiasReducer:
    """
    Step 5.3 - Bias Reduction
    Normalizes candidate responses to ensure fair evaluation across demographics.
    """
    def __init__(self):
        # Patterns to identify and remove PII or bias-inducing information
        self.PII_PATTERNS = [
            r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', # Potential Names
            r'\b\d{10}\b',                  # Phone numbers (simplified)
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', # Emails
        ]

    def purify_answer(self, text):
        """
        Removes bias-inducing information from the text before AI evaluation.
        """
        if not text:
            return ""
        
        purified = text
        for pattern in self.PII_PATTERNS:
            purified = re.sub(pattern, "[REDACTED]", purified)
            
        return purified

    def normalize_score(self, score, category):
        """
        Adjusts scores based on historical data to reduce systemic bias.
        In a full system, this would use statistical normalization.
        """
        # Placeholder for complex normalization logic
        return round(min(max(score, 0), 10), 2)

# Singleton instance
bias_reducer = BiasReducer()
