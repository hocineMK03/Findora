

import json
from pathlib import Path
class BigGramAlgo:
    
    def __init__(self):
        self.racine_metadata = {}
        self.processed_words = set()
        self.racine_mapping = {} 

    def retrieveRacines(self):
        script_dir = Path(__file__).resolve().parent
        filepaths =  script_dir / '..' / 're' / 'bigram.json'

        with open(filepaths, 'r') as file:
            filesData = json.load(file)

        words = list(filesData.keys())

        
        parent = {}

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y, new_racine=None):
            rootX = find(x)
            rootY = find(y)
            if rootX != rootY:
                if new_racine:  # Use the new root derived from `deBiGramed`
                    parent[rootX] = new_racine
                    parent[rootY] = new_racine
                    parent[new_racine] = new_racine
                else:  
                    parent[rootY] = rootX

        for i in range(len(words)):
            word1 = words[i]

            if word1 in self.processed_words:
                continue

            metadata1 = filesData[word1]
            bigrams1 = metadata1["bigrams"]
            document1 = metadata1["document"]

            
            racine_base = word1

            self.processed_words.add(word1)

            for j in range(i + 1, len(words)):
                word2 = words[j]
                
                metadata2 = filesData[word2]
                document2 = metadata2["document"]
                bigrams2 = metadata2["bigrams"]

                # Calculate similarity
                similarity = self.calculateDiceSimilarity(bigrams1, bigrams2)
                diceCoef, commonBigrams = similarity

                if diceCoef > 0.75:  # High similarity threshold
                    new_racine = self.deBiGramed(commonBigrams)
                    for word in [word1, word2, new_racine]:
                        if word not in parent:
                            parent[word] = word
                    union(word1, word2, new_racine)

                    # Find the updated racine base
                    racine_base = find(new_racine)
                    if racine_base not in self.racine_metadata:
                        self.racine_metadata[racine_base] = {
                            "words": [word1, word2],
                            "documents": [document1, document2]
                        }
                    else:
                        self.racine_metadata[racine_base]["words"].append(word2)
                        self.racine_metadata[racine_base]["documents"].append(document2)
                    self.processed_words.add(word2)

                    self.processed_words.add(word2)

        # Save the results to a file
        pathtobigramresult = script_dir / '..' / 're' / 'bigramresult.json'
        with open(pathtobigramresult, 'w') as file:
            json.dump(self.racine_metadata, file, indent=4, sort_keys=True)  
            
    def deBiGramed(self, bigrams):
        if not bigrams:
            return ""
        
        racine = bigrams[0][0]  # Start with the first character of the first bigram
        
        for bigram in bigrams:  # Append the second character of subsequent bigrams
            racine += bigram[1]
        
        return racine
    
    def calculateDiceSimilarity(self, bigrams1, bigrams2):
        common_bigrams, common_bigrams_count = self.findXCommonBigrams(bigrams1, bigrams2)
        bigrams1_count = len(bigrams1)
        bigrams2_count = len(bigrams2)
        
        dice_coef = 2 * common_bigrams_count / (bigrams1_count + bigrams2_count)
        
        return dice_coef, common_bigrams

    def findXCommonBigrams(self, bigrams1, bigrams2):
        common_bigrams = []
        if bigrams1[0][0] != bigrams2[0][0]:
            return common_bigrams, 0
        for bigram in bigrams1:
            if bigram in bigrams2:
                common_bigrams.append(bigram)
        
        return common_bigrams, len(common_bigrams)  # Return the common bigrams and their count
