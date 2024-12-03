# app.py
from flask import Flask
from src.routes.SearchRoutes import search  # Import the Blueprint object correctly
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["POST"]}})

# Register the blueprint with the app
app.register_blueprint(search)

if __name__ == '__main__':
    app.run(debug=True)
