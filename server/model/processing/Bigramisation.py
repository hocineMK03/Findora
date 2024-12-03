import json
from collections import defaultdict
from pathlib import Path
class Bigramisation:
    
    
    def processDocuments(self):
        script_dir = Path(__file__).resolve().parent
        filepaths = script_dir / '..' / 're' / 't.json'
        with open(filepaths, 'r') as file:
            filesData = json.load(file)  # Load JSON data
            
            word_metadata = defaultdict(list)
            
            for fileName, data in filesData.items():
                doc_metadata = self.processDocument(data, fileName)  # Process each document
                
                # Add the processed metadata for each word in the document
                for word, metadata in doc_metadata.items():
                    word_metadata[word] = metadata
                
        # Write all bigrams to a file at once after processing all documents
        pathtobigram=script_dir / '..' / 're' / 'bigram.json'
        with open(pathtobigram, 'w') as file:
            json.dump(word_metadata, file, indent=4, sort_keys=True)

    def processDocument(self, doc, fileName):
        doc_metadata = {}
        for word in doc:
            if len(word) > 1:  # Skip single character words
                wordBiGrams = self.generateCharBiGrams(word)  
                doc_metadata[word] = {
                    "bigrams": wordBiGrams,
                    "document": fileName
                }
        return doc_metadata

    def generateCharBiGrams(self, word):
        charBiGrams = []
        for i in range(len(word) - 1):  # Loop until the second last character
            bigram = word[i:i+2]  # Always take a pair of characters
            charBiGrams.append(bigram)  
        return charBiGrams
