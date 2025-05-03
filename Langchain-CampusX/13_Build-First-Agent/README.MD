# 🌦️ Streamlit Weather & Search Agent 🔍

This is a web application built with Streamlit that allows users to interact with a LangChain agent. The agent can answer questions by leveraging:

1.  **Large Language Model (LLM):** Powered by Groq for fast reasoning and response generation (using models like Llama 3).
2.  **Real-time Weather Data:** Fetches current weather conditions using the Weatherstack API via a custom LangChain tool.
3.  **Web Search:** Performs general knowledge lookups using the Tavily Search API via a dedicated LangChain tool.

The agent follows a ReAct (Reasoning and Acting) prompting strategy, allowing it to decide which tool to use (weather, search, or just the LLM) based on the user's query. The application displays the agent's step-by-step thought process for transparency.

## ✨ Features

*   **Interactive Web Interface:** Easy-to-use UI built with Streamlit.
*   **Natural Language Queries:** Ask questions in plain English.
*   **Combined Capabilities:** Handles questions requiring both weather information and general knowledge (e.g., "What's the weather like in the capital of France?").
*   **Real-time Data:** Uses live APIs for up-to-date weather and search results.
*   **Transparent Process:** Shows the agent's "Thoughts", "Actions" (tool calls), and "Observations" (tool results) as it works towards the final answer.
*   **Secure API Key Handling:** Requires users to enter their own API keys via the sidebar, ensuring keys are not hardcoded.
*   **Fast LLM Inference:** Leverages the Groq API for speedy language model responses.

## 📸 Screenshots

*(Add actual screenshots of your running application here)*

**Example Placeholder:**

*   *Main Interface:*
    ![Main Interface Placeholder](https://via.placeholder.com/600x400.png?text=App+Main+Interface)
    *(Shows the title, input box, and sidebar for API keys)*

*   *Agent Steps:*
    ![Agent Steps Placeholder](https://via.placeholder.com/600x300.png?text=Agent+Thinking+Process)
    *(Shows the "Agent Working..." section displaying Thought/Action/Observation steps)*

## 🛠️ Technology Stack

*   **Language:** Python 3.x
*   **Web Framework:** Streamlit
*   **LLM Orchestration:** LangChain
*   **LLM API:** Groq Cloud
*   **Weather API:** Weatherstack
*   **Search API:** Tavily AI
*   **Core Libraries:** `langchain`, `langchain-groq`, `streamlit`, `requests`, `python-dotenv`, `tavily-python`, `langchainhub`

## ⚙️ Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory-name>
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🔑 Configuration - API Keys

This application requires API keys from three services to function correctly. You need to provide them via the application's sidebar interface when you run it.

1.  **Groq API Key:** Get from [Groq Cloud Console](https://console.groq.com/keys).
2.  **Weatherstack API Key:** Get from [Weatherstack](https://weatherstack.com/) (a free tier is available).
3.  **Tavily API Key:** Get from [Tavily AI](https://tavily.com/) (a free tier is available).

**(Optional) Local Development using `.env`:**
For convenience during local development, you can create a `.env` file in the project's root directory and store your keys there. The application will load them automatically if the file exists. **Do not commit the `.env` file to Git!** Add `.env` to your `.gitignore` file.

```.env
GROQ_API_KEY="your_groq_api_key"
WEATHER_API="your_weatherstack_api_key"
TAVILY_API_KEY="your_tavily_api_key"