from src.config.db import connect_to_mongo

class Documents:
    
    def __init__(self):
      
        self.db = connect_to_mongo()  
        
      
        if self.db is None:
            raise Exception("Failed to connect to MongoDB")

        self.collection = self.db['documents']
        
        
    def retrieve_snippet(self, doc):
            
        document = self.collection.find_one({"filename": doc})
        snippet = document['content'][0:150]
            
        return snippet
                
    def retrieve_full_Content(self, doc):
            
        document = self.collection.find_one({"filename": doc})
        content = document['content']
            
        return content