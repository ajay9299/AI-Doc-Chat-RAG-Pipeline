from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config import Config
import os

class DocumentStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=Config.EMBEDDINGS_MODEL,
            encode_kwargs={"normalize_embeddings": True}
        )
        self.db = None
        self.load_or_create_index()
    
    def load_or_create_index(self):
        """Load existing FAISS index or create a new one"""
        try:
            if os.path.exists(Config.FAISS_INDEX_PATH):
                self.db = FAISS.load_local(
                    Config.FAISS_INDEX_PATH,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
            else:
                os.makedirs(Config.FAISS_INDEX_PATH, exist_ok=True)
                self.db = None
        except Exception as e:
            print(f"Error loading index: {e}")
            self.db = None
    
    def get_retriever(self):
        """Get retriever for querying documents"""
        if self.db is None:
            return None
        
        return self.db.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 3}
        )
    
    def retrieve(self, query):
        """Retrieve documents based on query"""
        retriever = self.get_retriever()
        if retriever is None:
            return []
        
        docs = retriever.invoke(query)
        return [d.page_content for d in docs]