
from collections import defaultdict
from src.models.KnowledgeTable import KnowledgeTable
from src.models.InverseTable import InverseTable

from src.models.Documents import Documents
from pathlib import Path
import re
class SearchServices:
    
    def tokenize(self,data):
        
        script_dir = Path(__file__).parent
        stoplist_path = script_dir / ".." / "stoplist" / "stoplist.txt"
        with open(stoplist_path, 'r') as file:
            stop_words = set(word.strip().lower() for word in file.readlines())

       
        words = data.split()
        words = [word.lower() for word in words]

        
        words = [word for word in words if word not in stop_words]

        
        words = [part for word in words for part in re.split(r'[^a-zA-Z0-9]+', word) if part]

        return words
    
    def initTheclasses(self):
        knowledge = KnowledgeTable()
        inversetable = InverseTable()
        documentscontent=Documents()
        return knowledge, inversetable, documentscontent
    def handleRetrieveDocs(self, data):
        knowledge, inversetable, documentscontent = self.initTheclasses()
        words = self.tokenize(data)
        
        # Retrieve racines from KnowledgeTable
        result = knowledge.retrieve_racines(words)
        result0 = result[0]  # Assuming this is the dictionary of racines
        
        
        resultdocs = {}
        document_details = {}
        document_scores = defaultdict(float)
        # Loop through the racines and map each key to its documents
        for racine, value in result0.items():
            if value is not None:
                # Retrieve documents for the current racine
                documents = inversetable.retrieve_documents(value)
                resultdocs[racine] = documents  
                for doc_id, score in documents.items():  
                    document_scores[doc_id] += score
                for doc_id, score in document_scores.items():
                    
                    document_content=documentscontent.retrieve_snippet(doc_id)
                    document_details[doc_id] = document_content
                
        sorted_documents = [
            {'doc_id': doc_id, 'score': score, 'snippet': document_details[doc_id]}
            for doc_id, score in sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
        ]
        
        return sorted_documents

    
    
    def handleSearchSpecificDoc(self, doc_id):
        documentscontent = Documents()
        content = documentscontent.retrieve_full_Content(doc_id)
        return content