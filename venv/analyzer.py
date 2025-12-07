from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List

class SentimentEngine:
    """
    Handles sentiment analysis logic for individual statements 
    and full conversation history.
    """
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_text(self, text: str) -> Dict[str, float]:
        """
        Analyzes a single string and returns raw scores.
        """
        return self.analyzer.polarity_scores(text)

    def get_sentiment_label(self, score: float) -> str:
        """
        Converts compound score to a readable label.
        Thresholds: > 0.05 Positive, < -0.05 Negative, else Neutral.
        """
        if score >= 0.05:
            return "Positive"
        elif score <= -0.05:
            return "Negative"
        else:
            return "Neutral"

    def analyze_conversation(self, history: List[Dict]) -> str:
        """
        Tier 1 Requirement: Analyze the entire conversation history.
        Includes 'Negativity Bias' logic for customer service contexts.
        """
        user_scores = [msg['score'] for msg in history if msg['role'] == 'User']
        
        if not user_scores:
            return "Neutral (No user input)"

        avg_score = sum(user_scores) / len(user_scores)
        min_score = min(user_scores) # The most negative moment

        # --- LOGIC FIX: Negativity Bias ---
        # If the average implies Neutral/Positive, BUT the user had a 
        # significant negative moment (score < -0.25), we override the 
        # overall rating to Negative.
        if avg_score > -0.15 and min_score < -0.25:
             final_label = "Negative"
             desc = " (Lingering Dissatisfaction)"
        else:
            final_label = self.get_sentiment_label(avg_score)
            desc = ""

        # Optional Tier 2: Detect trends
        trend = ""
        if len(user_scores) > 1:
            first = user_scores[0]
            last = user_scores[-1]
            if last > first + 0.2:
                trend = " - Mood Improving"
            elif last < first - 0.2:
                trend = " - Mood Worsening"

        return f"{final_label}{desc} (Avg: {avg_score:.2f}){trend}"