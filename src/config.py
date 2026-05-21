import os

class Config:
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    FAISS_INDEX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'faiss_index'))
    
    # Ollama settings
    OLLAMA_BASE_URL = "http://localhost:11434"
    OLLAMA_MODEL = "llama3"
    
    # Embeddings settings
    EMBEDDINGS_MODEL = "BAAI/bge-small-en"
    
    # Text splitting settings
    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 200