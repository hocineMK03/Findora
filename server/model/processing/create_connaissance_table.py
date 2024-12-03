import json
from pymongo import MongoClient

from pathlib import Path


def create_connaissance_table():
    script_dir1 = Path(__file__).resolve().parent
    filepaths = script_dir1 / '..' / 're' / 'bigramresult.json'

    with open(filepaths, 'r') as file:
        bigram_data = json.load(file)

    # Create a MongoDB connection
    client = MongoClient('mongodb://localhost:27017/')
    db = client['bigramdatabase']  # Replace with your database name
    collection = db['table_connaissance']  # Replace with your collection name


    knowledge_table = []

    for class_name, details in bigram_data.items():
        record = {
            "racine": class_name,
            
            "terms": details.get("words", [])
        }
        knowledge_table.append(record)

    # Insert the knowledge table into the MongoDB collection
    collection.insert_many(knowledge_table)

    print("Table de Connaissance has been created and stored in MongoDB.")
