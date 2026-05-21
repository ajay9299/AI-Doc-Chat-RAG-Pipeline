import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask
from config import Config
from routes.upload import upload_bp
from routes.query import query_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(upload_bp)
app.register_blueprint(query_bp)

@app.route('/')
def home():
    return {"message": "Flask PDF API is running Ajay 🚀"}

if __name__ == '__main__':
    app.run(debug=True, port=5000)