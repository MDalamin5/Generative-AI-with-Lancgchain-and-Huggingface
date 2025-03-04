
# Math Equation Solver

This project is an AI-based math equation solver built using various LangChain tools, aimed at providing step-by-step solutions to mathematical equations with explanations. It combines multiple machine learning models and document retrieval techniques to offer accurate answers based on a given mathematical problem and context.

## Features
- **Step-by-step Math Problem Solving**: The app provides detailed, step-by-step solutions to math equations with explanations, ensuring users understand the solving process.
- **Document-based Answering**: Uses a vector database to search for relevant documents from a PDF data source to answer user queries.
- **Model Integration**: The project integrates with several LLMs, including **Groq's Gemma2-9b** and **HuggingFace Embeddings**, to generate high-quality embeddings and answers.
- **Custom Prompting**: Custom prompts are utilized to ensure accurate and context-based answers.
- **Document Search**: Ability to search for relevant documents based on a user query and display their content.

## Technologies Used
- **Streamlit**: For the web interface, enabling easy interaction with the model.
- **LangChain**: For connecting language models, embeddings, and vector stores in an efficient chain.
- **Ollama**: For embedding generation (optional; can be switched for other models).
- **Groq**: For LLM integration to handle the question-answering process.
- **FAISS**: For efficient vector similarity search in the embedded document corpus.
- **HuggingFace Embeddings**: For generating document embeddings.
- **PyPDFDirectoryLoader**: To load and parse PDFs into documents for embedding.
- **RecursiveCharacterTextSplitter**: To split documents into manageable chunks for embedding.

## Installation

To run this project locally, follow the steps below:

1. Clone the repository:
   ```bash
   git clone https://github.com/MDalamin5/Generative-AI-with-Lancgchain-and-Huggingface
   cd Section-30-RAG-Document-QnA-with-GROQ
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables by creating a `.env` file in the project root directory and adding the following:
   ```bash
   GROQ_API_KEY=<your_groq_api_key>
   HF_TOKEN=<your_huggingface_token>
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

Once the app is running, you can interact with it via the following steps:

1. **Document Embedding**: When you first start the app, you can use the "Document Embedding" button to load PDF documents into the system and generate the corresponding embeddings.
2. **Enter an Equation**: Input a mathematical equation in the provided text box. The model will process the input and provide a step-by-step solution with an explanation.
3. **Document Similarity Search**: View relevant documents related to your query by expanding the "Document similarity search" section to see the context behind the response.

## How It Works

1. **Data Embedding**: The app processes a collection of PDF documents and splits them into chunks. These chunks are then embedded using a HuggingFace model and stored in a FAISS vector database.
2. **Query Handling**: When a user submits an equation, the app retrieves the most relevant documents based on the input query using the FAISS index and LLM integration.
3. **Answer Generation**: The model generates a step-by-step solution based on the retrieved documents and returns it to the user.

## Example

### Input:
- "What is the solution to 2x + 5 = 15?"

### Output:
- Step 1: "Isolate the variable: 2x = 15 - 5"
- Step 2: "Solve for x: x = 10 / 2"
- Step 3: "Final Answer: x = 5"

### Document Context:
- "This equation is a basic linear equation, where the goal is to isolate the variable on one side."

## Contributing

Feel free to fork the repository, open issues, and create pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License

---

### Note:
Ensure you have valid API keys for Groq and HuggingFace before running the project.
