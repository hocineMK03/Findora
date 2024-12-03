import json
from pymongo import MongoClient
from pathlib import Path


def create_inverse_file():
    
    script_dir = Path(__file__).resolve().parent
    filepaths = script_dir / '..' / 're' / 'bigramresult.json'
    with open(filepaths, 'r') as file:
        bigram_data = json.load(file)

    # Create a MongoDB connection
    client = MongoClient('mongodb://localhost:27017/')
    db = client['bigramdatabase']  # Replace with your database name
    collection = db['fichier_inverse']  # Replace with your collection name

    inverse_document_table = []

    # Iterate through each class in the bigram data
    for class_name, details in bigram_data.items():
        document_lists = []
        
        # Loop through each document and generate the necessary records
        for doc in details["documents"]:
            # Each document associated with the current class
            document_list = {
                "fileName": doc,
                "weight": 0,  # Add weight if needed (or leave as 0 for now)
            }
            document_lists.append(document_list)
        
        # Create a record for this class
        record = {
            "racine": class_name,
            "num_docs": len(details["documents"]),  # Number of documents
            "docs": document_lists
        }
        
        inverse_document_table.append(record)

    # Insert the knowledge table into the MongoDB collection
    collection.insert_many(inverse_document_table)

    print("Table de Connaissance has been created and stored in MongoDB.")
