import json
from pymongo import MongoClient
from pathlib import Path

def putdocstomongo():
    # MongoDB setup
    client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI
    db = client['bigramdatabase']  # Replace with your database name
    collection = db['documents']  # Replace with your collection name

    # Directory containing documents
    script_dir1 = Path(__file__).resolve().parent
    documents_dir = script_dir1 / '..' / 'documents'

    # Ensure the directory exists
    if not documents_dir.is_dir():
        print(f"The directory {documents_dir} does not exist.")
        return

    # Iterate through files and insert into MongoDB
    for file_path in documents_dir.glob('*'):  # You can specify file extensions if needed, e.g., '*.txt'
        if file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    document_data = {
                        'filename': file_path.name,
                        'content': content
                    }
                    collection.insert_one(document_data)
                    
            except Exception as e:
                print(f"Error reading {file_path.name}: {e}")



