# Sentiment Analysis Chatbot with LLM Integration

A "production-minded" chatbot that conducts natural conversations while performing real-time sentiment analysis. It features a modern web interface, message-level emotion tracking (Tier 2), and intelligent responses powered by the Groq LPU (Llama 3.1).

## How to Run

### Prerequisites
* Python 3.10 or higher
* A Groq API Key (Get one for free at [console.groq.com](https://console.groq.com))

### Installation
1.  Clone this repository or download the source code.
2.  Navigate to the project folder in your terminal.
3.  Install the required dependencies:
    ```bash
    pip install streamlit vaderSentiment groq
    ```

### Execution
1.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```
2.  A browser window will open automatically (usually at `http://localhost:8501`).
3.  **Enter your Groq API Key** in the sidebar to activate the LLM.
4.  Start chatting!

---

## Chosen Technologies

* **Python 3.x**: Core programming language.
* **Streamlit**: Used to build a responsive, chat-style web interface instead of a basic command-line tool.
* **VADER (Valence Aware Dictionary and sEntiment Reasoner)**: Chosen for the sentiment engine because it is specifically tuned for social media and short-text interactions. It handles emojis, slang, and capitalization better than traditional NLP pipelines.
* **Groq (Llama 3.1-8b)**: Serves as the conversational intelligence, replacing static "if/else" logic with dynamic, context-aware responses.

---

##  Explanation of Sentiment Logic

The sentiment engine (`analyzer.py`) uses a hybrid approach to ensure accuracy in customer service scenarios:

### 1. Individual Message Analysis (Tier 2)
* Every user input is passed through VADER to generate a `compound` score ranging from **-1.0 (Most Negative)** to **+1.0 (Most Positive)**.
* **Thresholds**:
    * `> 0.05`: **Positive**
    * `< -0.05`: **Negative**
    * Otherwise: **Neutral**

### 2. Conversation-Level Analysis (Tier 1)
* **Base Calculation**: The system calculates the average score of all user messages.
* **Negativity Bias (Custom Logic)**: In customer service, one bad experience often outweighs multiple neutral interactions.
    * *Rule*: If the **Average Score** is Neutral/Positive, BUT the **Minimum Score** (worst message) is below `-0.25`, the overall sentiment is overridden to **"Negative (Lingering Dissatisfaction)"**.
* **Trend Detection**: The system compares the score of the first message against the last message to detect if the user's mood is **Improving** or **Worsening** over time.

---

##  Status of Tier 2 Implementation

**Status: COMPLETED**

* **Message-Level Scoring**: The application evaluates every individual user message in real-time.
* **Visual Display**: Each user message is immediately followed by a color-coded sentiment tag (e.g., `Sentiment: Negative (-0.38)`) displayed in the chat interface.
* **Trend Summary**: The sidebar analytics include a "Mood Trend" indicator (e.g., "Mood Improving") as an optional enhancement.
##  Innovations & Bonus Features

* **LLM Integration**: Instead of hardcoded responses, the bot uses **Llama 3.1 via Groq** to understand context, display empathy, and answer complex queries.
* **Real-Time Dashboard**: A sidebar dashboard updates instantly with every message, showing the running average score and overall conversation mood.
* **Production Architecture**: The code is modular, separating the logic (`analyzer.py`), the AI service (`llm_service.py`), and the UI (`app.py`) for maintainability.