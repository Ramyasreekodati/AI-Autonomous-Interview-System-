import logging

logger = logging.getLogger(__name__)

class CheatingDetector:
    """
    Step 3.3 - Cheating Detection Logic
    Analyzes patterns of alerts to determine a probability of cheating.
    """
    def __init__(self):
        # Thresholds for various alert types
        self.LOOK_AWAY_THRESHOLD = 5
        self.MULTIPLE_FACES_THRESHOLD = 2
        self.PHONE_DETECTED_THRESHOLD = 1

    def analyze_session(self, alerts):
        """
        Input: list of alert objects {timestamp, type, confidence}
        Output: {cheating_detected: bool, risk_level: str, reason: str}
        """
        if not alerts:
            return {"cheating_detected": False, "risk_level": "Low", "reason": "No alerts triggered."}

        # Count frequencies
        counts = {
            "LOOK_AWAY": 0,
            "MULTIPLE_FACES": 0,
            "PHONE_DETECTED": 0,
            "BOOKS_DETECTED": 0
        }

        for alert in alerts:
            alert_type = alert.get("type")
            if alert_type in counts:
                counts[alert_type] += 1

        reasons = []
        is_suspicious = False
        risk_level = "Low"

        if counts["PHONE_DETECTED"] >= self.PHONE_DETECTED_THRESHOLD:
            reasons.append("Mobile device detected in frame")
            is_suspicious = True
            risk_level = "High"
        
        if counts["MULTIPLE_FACES"] >= self.MULTIPLE_FACES_THRESHOLD:
            reasons.append("Multiple people detected")
            is_suspicious = True
            risk_level = "High" if counts["MULTIPLE_FACES"] > 3 else "Medium"

        if counts["LOOK_AWAY"] >= self.LOOK_AWAY_THRESHOLD:
            reasons.append(f"Frequent lack of eye contact ({counts['LOOK_AWAY']} events)")
            is_suspicious = True
            if risk_level != "High":
                risk_level = "Medium"

        return {
            "cheating_detected": is_suspicious,
            "risk_level": risk_level,
            "reason": "; ".join(reasons) if reasons else "Normal behavior",
            "alert_counts": counts
        }

# Singleton instance
cheating_detector = CheatingDetector()
