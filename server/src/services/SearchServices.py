
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
        unique_words = list(set(words))
        wordsLength=len(words)
        word_frequencies = {}
        for word in words:
            word_frequencies[word] = word_frequencies.get(word, 0) + 1
        
        return unique_words,word_frequencies,wordsLength
    
    
    """     def calcuateRequestWeight(self,words):"""  
    
    def initTheclasses(self):
        knowledge = KnowledgeTable()
        inversetable = InverseTable()
        documentscontent=Documents()
        return knowledge, inversetable, documentscontent
    def handleRetrieveDocs(self, data):
        try:
            knowledge, inversetable, documentscontent = self.initTheclasses()
            words,word_freq,wordsLength= self.tokenize(data)
            # Retrieve racines from KnowledgeTable
            racines,racine_terms = knowledge.retrieve_racines(words)
            result0 = racines  
            
            
            resultdocs = {}
            document_details = {}
            document_scores = defaultdict(float)
            
            for racine, value in result0.items():
                if value is not None:
                
                    documents = inversetable.retrieve_documents(value)
                    resultdocs[racine] = documents  
                    for doc_id, score in documents.items():
                        # we have the freq of each term now we need to regroup them with each other term of the racine
                        theRacinefreq = 0
                        
                        for word in word_freq:
                            if word in racine_terms[racine]:
                                theRacinefreq += word_freq[word]
                        
                        
                        
                        thescore=theRacinefreq 
                        
                        thescore=thescore * score 
                        
                        #added vectorial model
                        document_scores[doc_id] += score *theRacinefreq
                    
                    for doc_id, score in list(document_scores.items()):  
                        if score != 0:
                            
                            document_content = documentscontent.retrieve_snippet(doc_id)
                            document_details[doc_id] = document_content
                        else:
                            # to remove  this will remove any score of 0
                            del document_scores[doc_id]
                    
            sorted_documents = [
                {'doc_id': doc_id, 'score': score, 'snippet': document_details[doc_id]}
                for doc_id, score in sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
            ]
            
            
                
            
            return sorted_documents
        except Exception as e:
            print(e)
            return str(e)

    
    
    def handleSearchSpecificDoc(self, doc_id):
        documentscontent = Documents()
        content = documentscontent.retrieve_full_Content(doc_id)
        return content