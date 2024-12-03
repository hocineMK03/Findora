from pymongo import MongoClient
import json

from pathlib import Path
# Create a MongoDB connection


def update_inverse_file():
    
    client = MongoClient('mongodb://localhost:27017/')
    db = client['bigramdatabase']  # Use your database name
    inverse_collection = db['fichier_inverse']  # Collection where inverted index is stored
    knowledge_collection = db['table_connaissance']  # Collection with racines and terms

    script_dir = Path(__file__).resolve().parent
    inverted_index_file = script_dir / '..' / 're' / 'inverted_index.json'
    with open(inverted_index_file, 'r') as file:
        inverted_index = json.load(file)

    # Function to retrieve TF-IDF from the inverted index
    def get_tfidf(term, doc_id):
    
        if term in inverted_index:
            for entry in inverted_index[term]:
                if entry["doc_id"] == doc_id:
                    return entry["weight"]
        return 0 


    for racine_record in knowledge_collection.find():
        class_name = racine_record.get("racine", "")
        terms = racine_record.get("terms", [])  
        
        
        for doc_data in inverse_collection.find({"racine": class_name}):
            for doc in doc_data.get('docs', []): 
                doc_id = doc.get('fileName', '')  
                if not doc_id:
                    continue  
                
                total_weight = 0

                
                for term in terms:
                    tfidf_value = get_tfidf(term, doc_id)
                    total_weight += tfidf_value  

                
                doc['weight'] = total_weight

            inverse_collection.update_one(
                {"_id": doc_data["_id"]}, 
                {"$set": {"docs": doc_data['docs']}} 
            )

    print("Weights have been calculated and updated for each document.")
