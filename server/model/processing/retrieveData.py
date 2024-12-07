

import os 
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json
from collections import defaultdict
import math
path='../t'
from pathlib import Path
os.chdir(path)



    
        
        

def processTFIDFTable():
    filepaths = "../re/t.json"
    with open(filepaths, 'r') as file:
        filesData = json.load(file)
        tfTable = {}
        
        termDocFreq = {}  
        for fileName, data in filesData.items():
            tfTable[fileName] = calculateTF(data)
            seen_terms_in_document = set()
        
            for word in data:
                if word not in seen_terms_in_document:
                    seen_terms_in_document.add(word)
                    
                    # Update the document frequency for each term   
                    if word in termDocFreq:
                        termDocFreq[word] += 1
                    else:
                        termDocFreq[word] = 1
        
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
                
                invertedIndex[term].append({"doc_id": filename, "weight": tfidf})
        
        # Step 4: Write the inverted index (fichier inverse) to a file """
        
        
        output_data = {}
        for fileName, tf in tfTable.items():
            for term, tf_value in tf.items():
                if term not in output_data:
                    output_data[term] = {
                        'termDocFreq': termDocFreq[term],
                        'tf': {}
                    }
                output_data[term]['tf'][fileName] = tf_value
                
            
        with open('../re/test.json', 'w') as file:
            json.dump(output_data, file, indent=4, sort_keys=True)

def calculateTF(data):
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
    
def retrieveRacines():
        script_dir = Path(__file__).resolve().parent
        filepaths =  script_dir / '..' / 're' / 'bigram.json'

        with open(filepaths, 'r') as file:
            filesData = json.load(file)

        words = list(filesData.keys())

        # Union-Find Data Structure for grouping similar terms together
        parent = {}
        racine_metadata = {}
        processed_words = set()
        racine_mapping = {}
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            rootX = find(x)
            rootY = find(y)
            if rootX != rootY:
                parent[rootY] = rootX

        for i in range(len(words)):
            word1 = words[i]

            if word1 in processed_words:
                continue

            metadata1 = filesData[word1]
            bigrams1 = metadata1["bigrams"]
            document1 = metadata1["document"]

           
            racine_base = word1

            processed_words.add(word1)

            for j in range(i + 1, len(words)):
                word2 = words[j]
                
                metadata2 = filesData[word2]
                document2 = metadata2["document"]
                bigrams2 = metadata2["bigrams"]

                # Calculate similarity
                similarity = calculateDiceSimilarity(bigrams1, bigrams2)
                diceCoef, commonBigrams = similarity

                if diceCoef > 0.75:  # High similarity threshold
                    # Merge the two terms into the same racine
                    if word2 not in parent:
                        parent[word2] = word2

                    #to fix 
                    
                    """ racine_base=deBiGramed(commonBigrams)
                    union(racine_base, word2)
                    racine_base = find(word1) """
                    union(word1, word2)
                    racine_base = find(word1)
                    
                    
                    
                    if racine_base not in racine_metadata:
                        racine_metadata[racine_base] = {
                            "words": [word1, word2],
                            "documents": [document1, document2]
                        }
                    else:
                        racine_metadata[racine_base]["words"].append(word2)
                        racine_metadata[racine_base]["documents"].append(document2)

                    processed_words.add(word2)

        # Save the results to a file
        pathtobigramresult = script_dir / '..' / 're' / 'bigramresult.json'
        with open(pathtobigramresult, 'w') as file:
            json.dump(racine_metadata, file, indent=4, sort_keys=True) 

            
def deBiGramed(bigrams):
    if not bigrams:
        return ""
    
    # Start with the first character of the first bigram
    racine = bigrams[0][0]
    
    # Append the second character of subsequent bigrams
    for bigram in bigrams:
        racine += bigram[1]
    
    return racine
    
def calculateDiceSimilarity(bigrams1, bigrams2):
   
    common_bigrams, common_bigrams_count = findXCommonBigrams(bigrams1, bigrams2)
    bigrams1_count = len(bigrams1)
    bigrams2_count = len(bigrams2)
    
    
    dice_coef = 2 * common_bigrams_count / (bigrams1_count + bigrams2_count)
    
    
    return dice_coef, common_bigrams


def findXCommonBigrams(bigrams1, bigrams2):
    common_bigrams = []
    if(bigrams1[0][0]!=bigrams2[0][0]):
        return common_bigrams, 0
    for bigram in bigrams1:
        if bigram in bigrams2:
            common_bigrams.append(bigram)
    
    # Return the common bigrams and their count as a tuple
    return common_bigrams, len(common_bigrams)
    
    
def processDocuments():
    filepaths = "../re/t.json"  # Path to your JSON file with documents
    with open(filepaths, 'r') as file:
        filesData = json.load(file)  # Load JSON data
        
        word_metadata = defaultdict(list)
        
        for fileName, data in filesData.items():
            doc_metadata = processDocument(data,fileName)  # Process each document
            
            
            # Add the processed metadata for each word in the document
            for word, metadata in doc_metadata.items():
                word_metadata[word] = metadata
            
    
    # Write all bigrams to a file at once after processing all documents
    with open('../re/bigram.json', 'w') as file:
        json.dump(word_metadata, file, indent=4, sort_keys=True)
    

def processDocument(doc, fileName):
    doc_metadata = {}
    for word in doc:
        if len(word) > 1:  # Skip single character words
            wordBiGrams = generateCharBiGrams(word)  
            doc_metadata[word] = {
                "bigrams": wordBiGrams,
                "document": fileName
            }
    return doc_metadata

def generateCharBiGrams(word):
    charBiGrams = []
    for i in range(len(word) - 1):  # Loop until the second last character
        bigram = word[i:i+2]  # Always take a pair of characters
        charBiGrams.append(bigram)  
    return charBiGrams

def retrieveStopList():
    stopListPath='../stoplist/stoplist.txt'
    with open(stopListPath, 'r') as file:
        stopList = file.read().split()
        return stopList
def transformFile(filepath):
    theStopList=retrieveStopList()
    thread_name = threading.current_thread().name
    """ print(f"Thread {thread_name} is processing file: {filepath}") """
    try:
        with open(filepath, 'r') as file:
           
            content = file.read()
            words = content.split()
            
            # Convert all words to lowercase
            words = [word.lower() for word in words]

            # Remove words that are in the stop list
            words = [word for word in words if word not in theStopList]

            # Split words containing special characters into separate parts and keep the words intact
            words = [part for word in words for part in re.split(r'[^a-zA-Z0-9]+', word) if part]
        """ print(f"Thread {thread_name} completed processing file: {filepath}") """
        return words  
    except Exception as e:
        print(f"Error processing file {filepath}: {e}")
        return []



def retrieve_text_paths():
    filepaths = []
    for file in os.listdir():
        filepaths.append(file)
        
        
    return filepaths
def retrieve_text_files():
    filesData={}
    
    max_workers=5
    filepaths=retrieve_text_paths()
    with ThreadPoolExecutor(max_workers = max_workers) as executor:
        future_to_path ={executor.submit(transformFile, file): file for file in filepaths}

   
        for f in as_completed(future_to_path):
            # Get the results
            
            try:
                fileName = future_to_path[f]
                data = f.result()
                filesData[fileName]=data
                
            except Exception as exc:
                print('%r generated an exception: %s' % (fileName, exc))
        
    
    
    
    
    with open('../re/t.json', 'w') as file:
        json.dump(filesData, file, indent=4, sort_keys=True)
    
    print(len(filesData))
    return filesData
    
        
       
    


start_time = time.perf_counter()
""" retrieve_text_files()
processDocuments()
retrieveRacines() """


processTFIDFTable()
end_time = time.perf_counter()
print(end_time-start_time)

