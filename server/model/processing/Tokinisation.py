import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
class Tokinisation:
    def __init__(self, path="../documents", stoplist_path="../stoplist/stoplist.txt"):
        script_dir = Path(__file__).resolve().parent
        self.path = script_dir / ".." / "documents"
        self.stoplist_path = script_dir / ".." / "stoplist" / "stoplist.txt"

    def retrieveStopList(self):
        with open(self.stoplist_path, 'r') as file:
            stopList = file.read().split()
            return stopList

    def transformFile(self, filepath):
        theStopList = self.retrieveStopList()
        thread_name = threading.current_thread().name
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

            return words
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")
            return []

    def retrieve_text_paths(self):
        # Return full paths to avoid chdir issues
        return [os.path.join(self.path, file) for file in os.listdir(self.path)]

    def retrieve_text_files(self):
        filesData = {}
        max_workers = 5
        filepaths = self.retrieve_text_paths()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_path = {executor.submit(self.transformFile, file): file for file in filepaths}

            for f in as_completed(future_to_path):
                try:
                    fileName = os.path.basename(future_to_path[f])  # Get only the file name
                    data = f.result()
                    filesData[fileName] = data
                except Exception as exc:
                    print('%r generated an exception: %s' % (fileName, exc))
        script_dir = Path(__file__).resolve().parent
        pathtodumpjson=script_dir / '..' / 're' / 't.json'
        with open(pathtodumpjson, 'w') as file:
            json.dump(filesData, file, indent=4, sort_keys=True)

        print(len(filesData))
        return filesData
