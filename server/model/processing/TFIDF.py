
import json
import math
from pathlib import Path
class TFIDF:
    
    def processTFIDFTable(self):
        script_dir = Path(__file__).resolve().parent
        filepaths = script_dir / '..' / 're' / 't.json'
     
        with open(filepaths, 'r') as file:
            filesData = json.load(file)
            tfTable = {}
            
            termDocFreq = {}  # Will store the document frequency for each term
            
            # Step 1: Calculate TF for each document and count document frequency for IDF
            for fileName, data in filesData.items():
                tfTable[fileName] = self.calculateTF(data)
                
                # Update the document frequency for each term   
                seen_terms_in_document = set()
            
                for word in data:
                    if word not in seen_terms_in_document:
                        seen_terms_in_document.add(word)
                        
                        # Update the document frequency for each term   
                        """ if word in termDocFreq:
                            termDocFreq[word] += 1
                        else:
                            termDocFreq[word] = 1 """
            
            totaldocs = len(filesData)
            idfTable = {}
            
            """ # Step 2: Calculate IDF for each term
            for term, docFreq in termDocFreq.items():
                if docFreq == 0:
                    continue  # Skip terms that appear in no documents (shouldn't happen)
            
                idf = math.log10(totaldocs / docFreq)
                
                # Optional: Add a threshold for very small values to avoid infinite IDF
                if idf < 0:
                    idf = 0

                idfTable[term] = idf
            
            # Step 3: Calculate TF-IDF for each term in each document and build inverted index
            invertedIndex = {}
            
            for filename, tf in tfTable.items():
                for term, tfValue in tf.items():
                    tfidf = tfValue * idfTable.get(term, 0)  # Get the IDF, default to 0 if not present
                    
                    # Add to the inverted index
                    if term not in invertedIndex:
                        invertedIndex[term] = []
                    
                    invertedIndex[term].append({"doc_id": filename, "weight": tfidf}) """
            output_data = {}
            for fileName, tf in tfTable.items():
                for term, tf_value in tf.items():
                    # Check if the term is not in output_data
                    if term not in output_data:
                        output_data[term] = {
                            'tf': {}  # Ensure 'tf' is initialized for this term
                        }
                    # Now safely add the tf_value to the 'tf' dictionary
                    output_data[term]['tf'][fileName] = tf_value

            
            invertedIndexFile = script_dir / '..' / 're' / 'inverted_index.json'
            with open(invertedIndexFile, 'w') as file:
                """ json.dump(invertedIndex, file, indent=4, sort_keys=True) """
                json.dump(output_data, file, indent=4, sort_keys=True)

    def calculateTF(self,data):
        tf = {}
        for word in data:
            if word in tf:
                tf[word] += 1
            else:
                tf[word] = 1
        
        totalWords = len(data)
        for word, count in tf.items():
            tf[word] = count / totalWords  # Normalize by the total number of words
        
        return tf
    
    