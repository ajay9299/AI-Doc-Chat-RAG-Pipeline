# Flask PDF API

This project is a Flask application that provides an API for uploading PDF documents and querying processed documents. It is designed to handle PDF uploads, process the content, and allow users to query the processed data.

## Project Structure

```
src/
├── app.py                   # Application entry point (Flask server start)
├── config.py                # Configuration settings (env, paths, constants)
│
├── routes/                  # API layer (controllers)
│   ├── __init__.py
│   ├── upload.py            # PDF upload endpoint
│   └── query.py             # RAG query endpoint
│
├── services/                # Core business logic
│   ├── __init__.py
│   ├── pdf_processor.py     # PDF loading, chunking, preprocessing
│   ├── embedding_service.py # Embeddings generation
│   ├── vector_store.py      # FAISS vector DB operations
│   └── rag_service.py       # Retrieval + LLM response generation
│
├── models/                  # Data models / schemas
│   ├── __init__.py
│   └── document.py
│
├── utils/                   # Helper utilities
│   ├── __init__.py
│   ├── validators.py
│   └── logger.py
│
│
│
uploads/                     # Uploaded PDF files
│
├── requirements.txt
└── README.md
```

## ⚙️ How It Works

1. Upload PDF via API
2. Extract text using PyPDFLoader
3. Split into chunks
4. Convert chunks into embeddings
5. Store in FAISS
6. Query → retrieve relevant chunks
7. Send context to LLM → generate answer

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd flask-pdf-api
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   python src/app.py
   ```

## API Endpoints

### Upload PDF Document

- **Endpoint:** `POST http://localhost:5000/upload`
- **Payload:** multipart/form-data with a file field named `file` (type: File). The form key must be exactly `file`.
- **Example (curl):**
```
curl -X POST http://localhost:5000/upload \
   -F "file=@/path/to/document.pdf"
```
- **Response:** JSON object with fields `message`, `filename`, `chunks_created`, and `documents`.

### Query Processed Documents

- **Endpoint:** `POST http://localhost:5000/query`
- **Payload:** JSON object with a `query` field. Example: `{ "query": "What is the summary of section 2?" }`
- **Example (curl):**
```
curl -X POST http://localhost:5000/query \
   -H "Content-Type: application/json" \
   -d '{"query":"What is the summary of section 2?"}'
```
- **Response:** JSON object with fields `query`, `answer`, and `sources_count`.

### Ollama (LLM) — Docker

To run Ollama locally (the app expects it on port `11434`):

```
docker run --rm -p 11434:11434 ollama/ollama:latest
```

After the container is running, ensure `Config.OLLAMA_BASE_URL` is set to `http://localhost:11434` and the model you want (for example `llama3`) is available to the Ollama server. Start Ollama before calling the `/query` endpoint.

## Additional Information

- Ensure that the `uploads` directory exists for storing uploaded files.
- The `data` directory can be used for any additional files needed for processing.
- Modify the `requirements.txt` file to include any additional libraries as needed.
