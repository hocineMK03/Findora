from src.config.db import connect_to_mongo

class InverseTable:
    
    def __init__(self):
      
        self.db = connect_to_mongo()  
        
      
        if self.db is None:
            raise Exception("Failed to connect to MongoDB")

        self.collection = self.db['fichier_inverse']
        
        
    def retrieve_documents(self, racine):
        documents = {}
        
        # Find the record with the given racine
        racine_record = self.collection.find_one({"racine": racine})
        if not racine_record:
            return documents  # Return an empty dictionary if racine is not found

        # Extract 'docs' and retrieve 'fileName' and 'weight' for each document
        for doc in racine_record.get('docs', []):
            documents[doc['fileName']] = doc.get('weight', 0)  # Default weight to 0 if missing
        
        return documents
