# src/models/DocumentModel.py
from src.config.db import connect_to_mongo

class KnowledgeTable:
    
    def __init__(self):
      
        self.db = connect_to_mongo()  
        
      
        if self.db is None:
            raise Exception("Failed to connect to MongoDB")

        self.collection = self.db['table_connaissance']

    def retrieve_racines(self, words):
        racines = {}
        terms_and_documents = {}

        
        for word in words:
            
            word_data = self.collection.find_one({"terms": word})  
            
            if word_data:
                racine = word_data.get('racine', None)  
                

              
                if racine:
                    racines[word] = racine
                else:
                    racines[word] = "No racine found"
                
                
                terms_and_documents[racine] = {
                    "terms": word_data.get('terms', []),
                    
                }
            else:
                racines[word] = None
                terms_and_documents[word] = None

        return racines, terms_and_documents
        
