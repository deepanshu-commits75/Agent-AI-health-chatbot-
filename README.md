# Agent-AI-health-chatbot-
A RAG and Agent-based health chatbot built with LangChain
# Health Chatbot Agent 🩺

This project is an advanced, conversational AI health assistant built using LangChain, RAG (Retrieval-Augmented Generation), and an agentic framework. It is designed to provide accurate health information by leveraging both structured and unstructured data sources.

## ✨ Features

- **Multi-Tool Agent:** The agent can intelligently decide which tool to use based on the user's query:
  - **Hospital Directory:** Finds hospitals in any Indian state and can filter by pincode.
  - **Vaccination Schedule:** Provides official vaccination schedules for infants and pregnant women.
  - **Health Knowledge Base (RAG):** Answers general health questions about symptoms, diseases, and conditions by searching a vectorized database of medical documents.
- **Conversational Memory:** Remembers the context of the conversation to answer follow-up questions.
- **Interactive & User-Friendly:** Provides human-like, conversational responses instead of raw data.
- **Zero Hallucination:** Grounded in provided documents and data to ensure factual accuracy.

## 🛠️ Tech Stack

- **Framework:** LangChain
- **LLM:** Llama-3 (via Groq API for high-speed inference)
- **Vector Database:** ChromaDB
- **Embedding Model:** `sentence-transformers/all-mpnet-base-v2`

## 🚀 How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/health-chatbot-agent.git](https://github.com/YourUsername/health-chatbot-agent.git)
    cd health-chatbot-agent
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up API Key:**
    - Get a free API key from [Groq](https://console.groq.com/keys).
    - Set it as an environment variable:
      ```bash
      export GROQ_API_KEY='your_api_key_here'
      ```

4.  **Prepare Data:**
    - **Update the ChromaDB path** in `app.py` to point to your vector store.
    - Place your `hospital_directory` folder (containing the metadata and state JSONs) inside the `data/` directory.
    - Place your `vaccination_schedule.json` file inside the `data/` directory.

5.  **Run the application:**
    ```bash
    python app.py
    ```
