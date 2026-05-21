from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import Config

class PDFProcessor:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        self.embeddings = HuggingFaceEmbeddings(
            model_name=Config.EMBEDDINGS_MODEL,
            encode_kwargs={"normalize_embeddings": True}
        )
    
    def process_pdf(self, file_path):
        """Load PDF, split into chunks, and store in FAISS"""
        try:
            print(f"Processing PDF: {file_path}")
            # Load PDF
            loader = PyPDFLoader(file_path)

            print(f"Loading PDF from: {loader}")
            documents = loader.load()
            
            # Split into chunks
            chunks = self.splitter.split_documents(documents)

            print(f"Created {len(chunks)} chunks from PDF")
            
            # Store in FAISS
            db = FAISS.from_documents(chunks, self.embeddings)
            db.save_local(Config.FAISS_INDEX_PATH)
            print(f"FAISS index saved to: {Config.FAISS_INDEX_PATH}")
            return {
                "success": True,
                "chunks_created": len(chunks),
                "documents": len(documents)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }