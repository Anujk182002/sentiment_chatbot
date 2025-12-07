import os
from groq import Groq

class LLMEngine:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        # UPDATED MODEL ID: "llama-3.1-8b-instant" 
        # (Replacing the decommissioned "llama3-8b-8192")
        self.model = "llama-3.1-8b-instant"

    def get_response(self, conversation_history):
        """
        Generates a response using Groq based on full conversation history.
        """
        messages = [
            {
                "role": "system", 
                "content": "You are a helpful customer service chatbot. Be concise and polite."
            }
        ]

        for msg in conversation_history:
            role = "user" if msg["role"] == "User" else "assistant"
            messages.append({"role": role, "content": msg["content"]})

        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error connecting to Groq: {str(e)}"