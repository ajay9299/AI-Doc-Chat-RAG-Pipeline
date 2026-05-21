from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from services.pdf_processor import PDFProcessor
from utils.validators import allowed_file, validate_file_size
from config import Config

upload_bp = Blueprint('upload', __name__)


def ensure_upload_folder():
    upload_folder = Config.UPLOAD_FOLDER
    if os.path.exists(upload_folder):
        if not os.path.isdir(upload_folder):
            raise RuntimeError(
                f"Upload path exists and is not a directory: {upload_folder}"
            )
    else:
        os.makedirs(upload_folder, exist_ok=True)

ensure_upload_folder()
pdf_processor = PDFProcessor()

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are allowed"}), 400
    
    if not validate_file_size(file):
        return jsonify({"error": "File size exceeds 50MB limit"}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(file_path)

    print(f"File saved to: {file_path}")
    # Process the PDF
    result = pdf_processor.process_pdf(file_path)
    
    if result["success"]:
        return jsonify({
            "message": "File uploaded and processed successfully",
            "filename": filename,
            "chunks_created": result["chunks_created"],
            "documents": result["documents"]
        }), 200
    else:
        return jsonify({
            "error": "Failed to process PDF",
            "details": result["error"]
        }), 500

@upload_bp.route('/cleanup', methods=['POST'])
def cleanup_uploads():
    ensure_upload_folder()
    deleted_files = []

    for filename in os.listdir(Config.UPLOAD_FOLDER):
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            deleted_files.append(filename)

    return jsonify({
        "message": "Uploads folder cleaned",
        "deleted_files": deleted_files
    }), 200