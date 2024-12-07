import math
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
    documents_folder = script_dir / '..' / 'documents'
    
    inverted_index_file = script_dir / '..' / 're' / 'inverted_index.json'
    with open(inverted_index_file, 'r') as file:
        inverted_index = json.load(file)

    def count_documents():
        
        document_files = [f for f in documents_folder.iterdir() if f.is_file()]
        return len(document_files)
    
    documents_length = count_documents()
    
    def calculate_idf(doc_freq):
        return math.log10(documents_length / doc_freq) if doc_freq > 0 else 0

    def get_docs_for_term(term):
        if term in inverted_index:
            return inverted_index[term]["tf"].keys()  
        return []

    def get_tf(term, doc_id):
        if term in inverted_index and doc_id in inverted_index[term]["tf"]:
            return inverted_index[term]["tf"][doc_id]
        return 0
    
    for racine_record in knowledge_collection.find():
        class_name = racine_record.get("racine", "")
        terms = racine_record.get("terms", [])
        
       
        for doc_data in inverse_collection.find({"racine": class_name}):
            all_term_docs = set()  
            
            for term in terms:
                term_docs = get_docs_for_term(term)
                all_term_docs.update(term_docs)  # Accumulate all unique documents for this term

           
            num_unique_docs = len(all_term_docs)
            racine_idf = calculate_idf(num_unique_docs)
            for doc in doc_data.get('docs', []): 
                doc_id = doc.get('fileName', '')  
                if not doc_id:
                    continue  
                
                total_weight = 0
                for term in terms:
                    tf_value = get_tf(term, doc_id)
                    total_weight += tf_value

                
                total_weight *= racine_idf  
                doc['weight'] = total_weight

            inverse_collection.update_one(
                {"_id": doc_data["_id"]}, 
                {"$set": {"docs": doc_data['docs']}} 
            )

    print("Weights have been calculated and updated for each document.")
