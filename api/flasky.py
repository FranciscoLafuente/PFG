import os
from app import create_app
from flask_cors import CORS

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
CORS(app)

