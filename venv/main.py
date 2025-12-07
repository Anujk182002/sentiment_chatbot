import sys
from analyzer import SentimentEngine
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)

class ChatBot:
    def __init__(self):
        self.engine = SentimentEngine()
        self.history = []  # Stores full conversation context
        self.active = True

    def get_bot_response(self, text: str) -> str:
        """
        Simple response logic (Flexible per assignment).
        In a real scenario, this would connect to an LLM or intent matcher.
        """
        text = text.lower()
        if "sad" in text or "disappoint" in text:
            return "I'm sorry to hear that. How can I fix it?"
        elif "happy" in text or "good" in text:
            return "I'm glad you're having a good experience!"
        else:
            return "I understand. Please tell me more."

    def run(self):
        print(f"{Fore.CYAN}=== Chatbot Initialized (Type 'exit' to end) ==={Style.RESET_ALL}")
        
        while self.active:
            try:
                user_input = input(f"{Fore.GREEN}User: {Style.RESET_ALL}").strip()
                
                if not user_input:
                    continue

                if user_input.lower() in ['exit', 'quit']:
                    self.active = False
                    break

                # --- Tier 2: Per-Message Analysis ---
                scores = self.engine.analyze_text(user_input)
                compound_score = scores['compound']
                label = self.engine.get_sentiment_label(compound_score)

                # Display Sentiment immediately (Tier 2 requirement)
                color = Fore.YELLOW if label == "Neutral" else (Fore.GREEN if label == "Positive" else Fore.RED)
                print(f"{color}→ Sentiment: {label} ({compound_score}){Style.RESET_ALL}")

                # Store history for Tier 1
                self.history.append({
                    'role': 'User',
                    'content': user_input,
                    'score': compound_score
                })

                # Bot Response
                response = self.get_bot_response(user_input)
                print(f"{Fore.BLUE}Chatbot: {Style.RESET_ALL}{response}")
                
                self.history.append({
                    'role': 'Chatbot',
                    'content': response,
                    'score': 0 # We usually track user sentiment, not bot
                })

            except KeyboardInterrupt:
                self.active = False
                print("\n")

        # --- Tier 1: End of Conversation Analysis ---
        print(f"\n{Fore.CYAN}=== Conversation Summary ==={Style.RESET_ALL}")
        final_sentiment = self.engine.analyze_conversation(self.history)
        print(f"Overall Conversation Sentiment: {Fore.MAGENTA}{final_sentiment}{Style.RESET_ALL}")

if __name__ == "__main__":
    bot = ChatBot()
    bot.run()