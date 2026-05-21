from flask import Blueprint, request, jsonify
from langchain_community.llms import Ollama
from services.document_store import DocumentStore
from config import Config

query_bp = Blueprint('query', __name__)

# Initialize document store
doc_store = DocumentStore()

# Initialize Ollama LLM
llm = Ollama(
    model=Config.OLLAMA_MODEL,
    base_url=Config.OLLAMA_BASE_URL
)

@query_bp.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({"error": "No query provided"}), 400
    
    user_query = data['query']
    
    # Retrieve relevant documents
    context_docs = doc_store.retrieve(user_query)
    
    if not context_docs:
        return jsonify({"error": "No documents found. Please upload a PDF first."}), 400
    
    context = "\n\n".join(context_docs)
    
    prompt = f"""You are a helpful assistant.

Answer ONLY from the context below.
If answer is not present, say "I don't know".

Context:
{context}

Question:
{user_query}
"""
    
    try:
        response = llm.invoke(prompt)
        return jsonify({
            "query": user_query,
            "answer": response,
            "sources_count": len(context_docs)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500